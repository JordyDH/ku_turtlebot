# KuLeuven Campus de Nayer - Turtlebot project

## How to work
This project works with a single ros package (main_package).    
To create a node follow next steps.

### Create node file
Goto the src/main_package/main_package/ folder.
Create the node file : touch <node_name>.py

### Add node file to setup.py file
Open src/main_package/setup.py
At the end you will see 'console_scripts'. Add here your package like the other.

```python  
"<executable_name> = main_package.<node_name>:main"  
```

### Add node to the launch file
Open src/main_package/launch/_launch.py and add the next block in the list.
 
```python
launch_ros.actions.Node(
                package='main_package', executable='<executable_name>', output='screen',
                name=['<executable_name>']),
```

When you use a lib in python you will need to check the package.xml file to see if it is present.  
If not add this line with the lib name:  

```xml
<exec_depend> "lib name" </exec_depend>  
```

## Developers

## License
