# BlenTools
An add-on for Blender, with various macro's/presets to speed up your character design workflow.
The add-on includes little features, like seperating vertex groups from your mesh and storing them in your file, or a quick IK bone setup. A guide for using the add-on is worked on. The add-on is still very new, and most features are not ready yet.



To install the addon, download and extract the .zip file. Go to blenders preferences -> Add-ons -> Install and choose the "Final.py" file, click the "Install Add-on" button, and activate the addon by checking the checkbox.


## VertexSeperation
The addon isn't able to do very much currently (new functionality will be added in the future), but one of the already existing functions is separeting vertexgroups from your mesh and storing them in your file. To explain the reason why this is somethimes helpfull, let me give an example:

*You have a mesh with an armature parented to it with automatic weights, so you got one or more vertex groups from your bones. 
You also have a particle system on your mesh, to give the object hairs. This particle system uses a vertex group to control the density of the hairs. 
Then you want to adjust the vertex groups from the bones, and you want to use* Normalize *and* Auto Normalize *to normalize your vertex groups. The only problem is that when you normalize the vertex groups, also the vertex group which is used to control the density of the hairs will be effected, and likely you don't want this. Of course you can lock the vertex group used for the hairs, then the locked group wil not change, but it is still *

That is where this function of the addon comes in handy, the addon let you seperate the vertex group used for the hairs from your mesh, and it will store it on an invisible copy of the mesh in your file. Then you can change the vertex groups from the bones and normalize them without effecting the other vertex group.
