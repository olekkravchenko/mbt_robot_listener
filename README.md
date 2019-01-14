# mbt_robot_listener


Setup MBT Robot Listener example
-------------------------------

To clone project execute command in a Git Bash:

    git clone https://github.com/olekkravchenko/mbt_robot_listener.git


Executing from command line (Windows)
-------------------------------
    cd <mbt_listener_installation_folder>
    set PYTHONPATH=%PYTHONPATH%;<mbt_listener_installation_folder>
    robot --listener listeners.mbt_listener.MBTGeneratorListener:<generator_algorithm_name>:<path_to_model_yaml>:<max_number_of_transitions> --listener listeners.report_generator_listener.ReportGeneratorListener:<temporary_log_folder_name> mbt_test_suite.robot


Example:
-------------------------------
    robot --listener listeners.mbt_listener.MBTGeneratorListener:random_weighted:models\dut_model.yaml:25 --listener listeners.report_generator_listener.ReportGeneratorListener:logs mbt_test_suite.robot

Folder Structure:
-------------------------------
    dut - toy program under test. Common for script base testing and MBT
    listeners - interface 3 listener class, model transition generators. MBT only
    models - yaml test model, keywords to define preconditions, transitions and state verifications. MBT only
    resources - robot resource files that define interactions with DUT. Common for script base testing and MBT
