#!/bin/bash
cd ~/catkin_ws/src/pi3_robot_2019 
read -p "write the version, format (X.Y.Z):" version
if test -d "com/github/biorobaw/pi3_robot_messages/${version}"; then 
    read -p "Version already exists, do you wish to overwrite it (y/n)?" choice
    case "$choice" in 
      y|Y ) echo "Proceeding with operation";;
      * ) echo "Operation aborted" ; exit -1;;
    esac    
fi

genjava_message_artifacts --verbose -p pi3_robot_2019 && \
mvn install:install-file \
    -DgroupId=com.github.biorobaw \
    -DartifactId=pi3_robot_messages \
    -Dversion=${version} \
    -Dfile=../../devel/share/maven/org/ros/rosjava_messages/pi3_robot_2019/0.0.0/pi3_robot_2019-0.0.0.jar \
    -Dpackaging=jar \
    -DpomFile=../../devel/share/maven/org/ros/rosjava_messages/pi3_robot_2019/0.0.0/pi3_robot_2019-0.0.0.pom \
    -DlocalRepositoryPath=. \
    -DcreateChecksum=true && \
sed -i "s/>0.0.0</>${version}</g" com/github/biorobaw/pi3_robot_messages/${version}/pi3_robot_messages-${version}.pom && \
echo "Export succeeded" && exit 0
echo "Something went wrong :)"
exit -1
