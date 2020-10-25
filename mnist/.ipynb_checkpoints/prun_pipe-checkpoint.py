#!/usr/bin/env python
# coding: utf-8

# In[1]:


import kfp
import kfp.dsl as dsl
import kfp.onprem as onprem

def echo_op(text):
    return dsl.ContainerOp(
        name='echo',
        image='library/bash:4.4.23',
        command=['sh', '-c'],
        arguments=['echo "$0"', text],
    )

@dsl.pipeline(
    name='FMnistPipeline',
    description='mnist '
)
def fmnist_pipeline(learning_rate, dropout_rate,model_path,model_version):
    
    exit_task = echo_op("Done!")
    
    with dsl.ExitHandler(exit_task): 
        
        #vol component
        #fmnist_pvc = dsl.PipelineVolume(pvc="tfjob-data-volume", name="tfjob-data-volume")
        fmnist_vop = dsl.VolumeOp(
            name="0_fmnist-volume",
            resource_name="fmnist-pvc",
            modes=dsl.VOLUME_MODE_RWO,
            size="100Mi"
        )
        
        #base component
        mnist = dsl.ContainerOp(
            name='Train',
            image='khw2126/mnist-simple:D33F92CD',
            command=['python', '/app/Train.py'],
            arguments=[
                "--learning_rate", learning_rate,
                "--dropout_rate", dropout_rate,
                "--model_path", model_path,
                "--model_version", model_version
            ],
            pvolumes={"/result": fmnist_vop.volume}
        )
        
        #prun com
        prun = dsl.ContainerOp(
            name='prun',
            image='khw2126/prun:0.0.1',
            command=['python', '/app/pruning_code.py'],
            arguments=[
                "--model_path", model_path,
                "--model_version", model_version
            ],
            output_artifact_paths={'mlpipeline-metrics': '/mlpipeline-metrics.json'},
            pvolumes={"/result": mnist.volume}
        )
        
        #result com
        result = dsl.ContainerOp(
            name='list_list',
            image='library/bash:4.4.23',
            command=['ls', '-R', '/result'],
            pvolumes={"/result": prun.pvolume}
        )
        
        #order
        prun.after(mnist)

        result.after(prun)
    
#argument !![model_path, model_version]
#model_version: name
arguments = {'learning_rate': '0.001397',
             'dropout_rate': '0.18',
             'model_path':'/result/saved_model',
             'model_version': 'quant-aware' 
            }
    
if __name__ == '__main__':
    kfp.Client().create_run_from_pipeline_func(pipeline_func=fmnist_pipeline, 
                                               arguments=arguments)


# In[ ]:




