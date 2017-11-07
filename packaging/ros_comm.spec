Name:	ros-kinetic-comm
Version:	1.13.2
Release:	0
Summary:	ROS communications-related packages
License:	BSD
URL:		http://wiki.ros.org/ros_comm
Source0:	%{name}-%{version}.tar.gz
Source1001:	ros_comm.manifest
BuildRequires:	cmake
BuildRequires:	ros-kinetic-catkin
BuildRequires:	ros-kinetic-cpp-common
BuildRequires:	ros-kinetic-message-generation
BuildRequires:	ros-kinetic-rostime
BuildRequires:	ros-kinetic-rosunit
BuildRequires:	ros-kinetic-cpp-common
BuildRequires:	ros-kinetic-roscpp-serialization
BuildRequires:	ros-kinetic-rosgraph-msgs
BuildRequires:	ros-kinetic-message-runtime
BuildRequires:	ros-kinetic-std-msgs
BuildRequires:	ros-kinetic-std-srvs
BuildRequires:	ros-kinetic-genmsg
BuildRequires:	ros-kinetic-geneus
BuildRequires:	ros-kinetic-gencpp
BuildRequires:	ros-kinetic-genlisp
BuildRequires:	ros-kinetic-genpy
BuildRequires:	ros-kinetic-gennodejs
BuildRequires:	pkg-config
BuildRequires:	pkgconfig(boost)
BuildRequires:	liblz4-devel
BuildRequires:	python = 2.7
BuildRequires:	python-devel
BuildRequires:	libpython
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	gtest-devel
Requires:	ros-kinetic-roscpp
Requires:	ros-kinetic-rospy
Requires:	ros-kinetic-rosgraph-msgs
Requires:	ros-kinetic-std-srvs
Requires:	ros-kinetic-ros
Requires:	ros-kinetic-rosbag
Requires:	ros-kinetic-rosconsole
Requires:	ros-kinetic-rosgraph
Requires:	ros-kinetic-roslaunch
Requires:	ros-kinetic-roslisp
Requires:	ros-kinetic-rosmaster
Requires:	ros-kinetic-rosmsg
Requires:	ros-kinetic-rosnode
Requires:	ros-kinetic-rosout
Requires:	ros-kinetic-rosparam
Requires:	ros-kinetic-rosservice
Requires:	ros-kinetic-rostest
Requires:	ros-kinetic-rostopic
Requires:	ros-kinetic-topic-tools
Requires:	ros-kinetic-message-filters
Requires:	ros-kinetic-roswtf
Requires:	ros-kinetic-xmlrpcpp

%description
ROS communications-related packages, including core client libraries (roscpp, rospy, roslisp) and graph introspection tools (rostopic, rosnode, rosservice, rosparam) and other many tools (roslaunch, rosbag, rosbag_storage, rosmaster, rosmsg, rostest, topic_tools, rosout), utilities (message-filters, roslz4, roswtf, xmlrpcpp), and test suites.


%define __ros_build \
mkdir -p build && pushd build \
cmake .. -DCMAKE_INSTALL_PREFIX="%{__ros_install_path}" -DCMAKE_PREFIX_PATH="%{__ros_install_path};%{buildroot}%{__ros_install_path}" -DSETUPTOOLS_DEB_LAYOUT=OFF -DCATKIN_BUILD_BINARY_PACKAGE="1" \
make %{?_smp_mflags} \
popd \
%{nil}

%define __ros_in_build()	\
				pushd %{1} \
				%{__ros_build} \
				popd \
				%{nil}

%define __ros_in_install()	\
				pushd %{1} \
				%{__ros_install} \
				popd \
				%{nil}

%define __ros_in_pkg()	\
%package -n ros-kinetic-%{2} \
Summary:	ROS %{2} package \
%{nil}

%define __ros_in_files()	\
%description -n ros-kinetic-%{2} \
ROS %{2} package created from ros-kinetic-comm \
%files -n ros-kinetic-%{2} -f %{1}/build/install_manifest.txt \
%manifest ros_comm.manifest \
%defattr(-,root,root) \
%{nil}

%prep
%setup -q
cp %{SOURCE1001} .

%build
%{__ros_setup}

# To break circular dependency (BuildRequires: ros-kinetic-rosconsole from ros_comm)
%__ros_in_build tools/rosconsole
%__ros_in_install tools/rosconsole

# To break circular dependency (BuildRequires: ros-kinetic-xmlrcpp from ros_comm)
%__ros_in_build utilities/xmlrpcpp
%__ros_in_install utilities/xmlrpcpp

# To break circular dependency (BuildRequires: ros-kinetic-roslz4 from rosbag-storage)
%__ros_in_build utilities/roslz4
%__ros_in_install utilities/roslz4

# To break circular dependency (BuildRequires: ros-kinetic-rosbagstorage from rosbag)
%__ros_in_build tools/rosbag_storage
%__ros_in_install tools/rosbag_storage

# To break circular dependency (BuildRequires: ros-kinetic-roscpp from ros-kinetic-rosbag)
%__ros_in_build clients/roscpp
%__ros_in_install clients/roscpp

# To break circular dependency from topic_tools
%__ros_in_build tools/rostest
%__ros_in_install tools/rostest

# To break circular dependency (BuildRequires: ros-kinetic-topic-tools from ros-kinetic-rosbag)
%__ros_in_build tools/topic_tools
%__ros_in_install tools/topic_tools

%__ros_in_build tools/rosbag
%__ros_in_build tools/rosgraph
%__ros_in_build tools/roslaunch
%__ros_in_build tools/rosmaster
%__ros_in_build tools/rosmsg
%__ros_in_build tools/rosnode
%__ros_in_build tools/rosout
%__ros_in_build tools/rosparam
%__ros_in_build tools/rosservice
%__ros_in_build tools/rostopic

# To break circular dependency (BuildRequires: ros-kinetic-* from ros-kinetic-test-*)
%__ros_in_install tools/rosbag
%__ros_in_install tools/rosgraph
%__ros_in_install tools/roslaunch
%__ros_in_install tools/rosmaster
%__ros_in_install tools/rosparam
%__ros_in_install tools/rosservice
%__ros_in_install tools/rostopic

%__ros_in_build ros_comm


%__ros_in_build clients/rospy


%__ros_in_build test/test_rosbag
%__ros_in_build test/test_rosbag_storage
%__ros_in_build test/test_roscpp
%__ros_in_build test/test_rosgraph
%__ros_in_build test/test_roslaunch
%__ros_in_build test/test_roslib_comm
%__ros_in_build test/test_rosmaster

# To break circular dependency from test_rospy
%__ros_in_install test/test_rosmaster

%__ros_in_build test/test_rosparam

# Somehow genmsg is weirdly acting (cannot find cmake of rosmaster)
mkdir -p test/test_rospy/build/devel/share
pushd test/test_rospy/build/devel/share
ln -s %{buildroot}%{__ros_install_path}/share/* .
popd
pushd test/test_rospy/build/devel
ln -s ../../../../tools/rostest/include include
popd

%__ros_in_build test/test_rospy
%__ros_in_build test/test_rosservice
%__ros_in_build test/test_rostopic

%__ros_in_build utilities/message_filters
%__ros_in_build utilities/roswtf

%install
rm -Rf %{buildroot}/*
%{__ros_setup}
# Workaround to avoid [  121s] Found '/home/abuild/rpmbuild/BUILDROOT/ros-kinetic-comm-1.13.2-0.x86_64' in installed files; aborting

# There are damn dependencies between the install scripts. The order matters!
%__ros_in_install tools/rosconsole
%__ros_in_install utilities/xmlrpcpp
%__ros_in_install utilities/roslz4
%__ros_in_install tools/rosbag_storage
%__ros_in_install clients/roscpp
%__ros_in_install tools/rostest
%__ros_in_install tools/topic_tools

%__ros_in_install tools/rosbag
%__ros_in_install tools/rosgraph
%__ros_in_install tools/roslaunch
%__ros_in_install tools/rosmaster
%__ros_in_install tools/rosmsg
%__ros_in_install tools/rosnode
%__ros_in_install tools/rosout
%__ros_in_install tools/rosparam
%__ros_in_install tools/rosservice
%__ros_in_install tools/rostopic

%__ros_in_install ros_comm

%__ros_in_install clients/rospy

%__ros_in_install test/test_rosbag_storage
%__ros_in_install test/test_rosbag
%__ros_in_install test/test_roscpp
%__ros_in_install test/test_rosgraph
%__ros_in_install test/test_roslaunch
%__ros_in_install test/test_roslib_comm
%__ros_in_install test/test_rosmaster
%__ros_in_install test/test_rosparam
%__ros_in_install test/test_rospy
%__ros_in_install test/test_rosservice
%__ros_in_install test/test_rostopic

%__ros_in_install utilities/message_filters
%__ros_in_install utilities/roswtf

%files -f ros_comm/build/install_manifest.txt
%manifest ros_comm.manifest
%defattr(-,root,root)


%__ros_in_pkg clients/roscpp	roscpp
Requires:	ros-kinetic-cpp-common >= 0.3.17
Requires:	ros-kinetic-message-runtime
Requires:	ros-kinetic-rosconsole
Requires:	ros-kinetic-roscpp-serialization
Requires:	ros-kinetic-roscpp-traits >= 0.3.17
Requires:	ros-kinetic-rosgraph-msgs >= 1.10.3
Requires:	ros-kinetic-rostime
Requires:	ros-kinetic-std-msgs
Requires:	ros-kinetic-xmlrpcpp
%__ros_in_files clients/roscpp	roscpp

%__ros_in_pkg clients/rospy	rospy
Requires:	ros-kinetic-genpy
Requires:	python-numpy
Requires:	python-rospkg
Requires:	python-yaml
Requires:	ros-kinetic-roscpp
Requires:	ros-kinetic-rosgraph
Requires:	ros-kinetic-rosgraph-msgs >= 1.10.3
Requires:	ros-kinetic-roslib
Requires:	ros-kinetic-std-msgs
%__ros_in_files clients/rospy	rospy
%{__ros_install_path}/lib/python2.7/site-packages/rospy*
%{__ros_install_path}/lib/python2.7/site-packages/rospy/*

%__ros_in_pkg test/test_rosbag	test-rosbag
%__ros_in_files test/test_rosbag	test-rosbag

%__ros_in_pkg test/test_rosbag_storage	test-rosbag_storage
Requires:	ros-kinetic-rosbag-storage
Requires:	ros-kinetic-std-msgs
%__ros_in_files test/test_rosbag_storage	test-rosbag_storage

%__ros_in_pkg test/test_roscpp	test-roscpp
Requires:	ros-kinetic-message-runtime
Requires:	ros-kinetic-rosconsole
Requires:	ros-kinetic-rosgraph-msgs
Requires:	ros-kinetic-std-msgs
Requires:	ros-kinetic-std-srvs
Requires:	ros-kinetic-xmlrpcpp
%__ros_in_files test/test_roscpp	test-roscpp

%__ros_in_pkg test/test_rosgraph	test-rosgraph
%__ros_in_files test/test_rosgraph	test-rosgraph

%__ros_in_pkg test/test_roslaunch	test-roslaunch
%__ros_in_files test/test_roslaunch	test-roslaunch

%__ros_in_pkg test/test_roslib_comm	test-roslib_comm
%__ros_in_files test/test_roslib_comm	test-roslib_comm

%__ros_in_pkg test/test_rosmaster	test-rosmaster
%__ros_in_files test/test_rosmaster	test-rosmaster

%__ros_in_pkg test/test_rosparam	test-rosparam
%__ros_in_files test/test_rosparam	test-rosparam

%__ros_in_pkg test/test_rospy	test-rospy
Requires:	python-numpy
Requires:	python-psutil
Requires:	ros-kinetic-rosbuild
Requires:	ros-kinetic-rosgraph
Requires:	ros-kinetic-rospy
%__ros_in_files test/test_rospy	test-rospy
%{__ros_install_path}/share/common-lisp/ros/test_rospy/*
%{__ros_install_path}/share/gennodejs/ros/test_rospy/*
%{__ros_install_path}/share/roseus/ros/test_rospy/*

%__ros_in_pkg test/test_rosservice	test-rosservice
%__ros_in_files test/test_rosservice	test-rosservice

%__ros_in_pkg test/test_rostopic	test-rostopic
%__ros_in_files test/test_rostopic	test-rostopic

%__ros_in_pkg tools/rosbag	rosbag
Requires:	boost
Requires:	ros-kinetic-genmsg
Requires:	ros-kinetic-genpy
Requires:	python-rospkg
Requires:	ros-kinetic-rosbag-storage
Requires:	ros-kinetic-rosconsole
Requires:	ros-kinetic-roscpp
Requires:	ros-kinetic-roslib
Requires:	ros-kinetic-rospy
Requires:	ros-kinetic-std-srvs
Requires:	ros-kinetic-topic-tools
Requires:	ros-kinetic-xmlrpcpp
%__ros_in_files tools/rosbag	rosbag

%__ros_in_pkg tools/rosbag_storage	rosbag-storage
Requires:	boost
Requires:	bzip2
Requires:	ros-kinetic-cpp-common >= 0.3.17
Requires:	libconsole-bridge
Requires:	ros-kinetic-roscpp-serialization
Requires:	ros-kinetic-roscpp-traits >= 0.3.17
Requires:	ros-kinetic-rostime
Requires:	ros-kinetic-roslz4
%__ros_in_files tools/rosbag_storage	rosbag-storage
%{__ros_install_path}/bin/rosbag
%{__ros_install_path}/lib/python2.7/site-packages/rosbag*
%{__ros_install_path}/lib/python2.7/site-packages/rosbag/*

%__ros_in_pkg tools/rosconsole	rosconsole
Requires:	apr
Requires:	ros-kinetic-cpp-common
Requires:	log4cxx
Requires:	ros-kinetic-rosbuild
Requires:	ros-kinetic-rostime
%__ros_in_files tools/rosconsole	rosconsole
%{__ros_install_path}/bin/rosconsole

%__ros_in_pkg tools/rosgraph	rosgraph
Requires:	python-netifaces
Requires:	python-rospkg
%__ros_in_files tools/rosgraph	rosgraph
%{__ros_install_path}/bin/rosgraph
%{__ros_install_path}/lib/python2.7/site-packages/rosgraph*
%{__ros_install_path}/lib/python2.7/site-packages/rosgraph/*

%__ros_in_pkg tools/roslaunch	roslaunch
Requires:	python-paramiko
Requires:	python-rospkg >= 1.0.37
Requires:	python-yaml
Requires:	ros-kinetic-rosclean
Requires:	ros-kinetic-rosgraph-msgs
Requires:	ros-kinetic-roslib
Requires:	ros-kinetic-rosmaster >= 1.11.16
Requires:	ros-kinetic-rosout
Requires:	ros-kinetic-rosparam
Requires:	ros-kinetic-rosunit >= 1.13.3
%__ros_in_files tools/roslaunch	roslaunch
%{__ros_install_path}/bin/roscore
%{__ros_install_path}/bin/roslaunch
%{__ros_install_path}/bin/roslaunch-complete
%{__ros_install_path}/bin/roslaunch-deps
%{__ros_install_path}/bin/roslaunch-logs
%{__ros_install_path}/lib/python2.7/site-packages/roslaunch*
%{__ros_install_path}/lib/python2.7/site-packages/roslaunch/*

%__ros_in_pkg tools/rosmaster	rosmaster
Requires:	ros-kinetic-rosgraph
Requires:	python-defusedxml
%__ros_in_files tools/rosmaster	rosmaster
%{__ros_install_path}/bin/rosmaster
%{__ros_install_path}/lib/python2.7/site-packages/rosmaster*
%{__ros_install_path}/lib/python2.7/site-packages/rosmaster/*

%__ros_in_pkg tools/rosmsg	rosmsg
Requires:	ros-kinetic-catkin >= 0.6.4
Requires:	ros-kinetic-genmsg
Requires:	python-rospkg
Requires:	ros-kinetic-rosbag
Requires:	ros-kinetic-roslib
%__ros_in_files tools/rosmsg	rosmsg
%{__ros_install_path}/bin/rosmsg
%{__ros_install_path}/bin/rosmsg-proto
%{__ros_install_path}/bin/rossrv
%{__ros_install_path}/lib/python2.7/site-packages/rosmsg*
%{__ros_install_path}/lib/python2.7/site-packages/rosmsg/*

%__ros_in_pkg tools/rosnode	rosnode
Requires:	ros-kinetic-rosgraph
Requires:	ros-kinetic-rostopic
%__ros_in_files tools/rosnode	rosnode
%{__ros_install_path}/bin/rosnode
%{__ros_install_path}/lib/python2.7/site-packages/rosnode*
%{__ros_install_path}/lib/python2.7/site-packages/rosnode/*

%__ros_in_pkg tools/rosout	rosout
Requires:	ros-kinetic-roscpp
Requires:	ros-kinetic-rosgraph-msgs
%__ros_in_files tools/rosout	rosout

%__ros_in_pkg tools/rosparam	rosparam
Requires:	python-yaml
Requires:	ros-kinetic-rosgraph
%__ros_in_files tools/rosparam	rosparam
%{__ros_install_path}/bin/rosparam
%{__ros_install_path}/lib/python2.7/site-packages/rosparam*
%{__ros_install_path}/lib/python2.7/site-packages/rosparam/*

%__ros_in_pkg tools/rosservice	rosservice
Requires:	ros-kinetic-genpy
Requires:	ros-kinetic-rosgraph
Requires:	ros-kinetic-roslib
Requires:	ros-kinetic-rospy
Requires:	ros-kinetic-rosmsg
%__ros_in_files tools/rosservice	rosservice
%{__ros_install_path}/bin/rosservice
%{__ros_install_path}/lib/python2.7/site-packages/rosservice*
%{__ros_install_path}/lib/python2.7/site-packages/rosservice/*

%__ros_in_pkg tools/rostest	rostest
Requires:	boost
Requires:	ros-kinetic-rosgraph
Requires:	ros-kinetic-roslaunch
Requires:	ros-kinetic-rosmaster
Requires:	ros-kinetic-rospy
Requires:	ros-kinetic-rosunit
%__ros_in_files tools/rostest	rostest
%{__ros_install_path}/bin/rostest
%{__ros_install_path}/lib/python2.7/site-packages/rostest*
%{__ros_install_path}/lib/python2.7/site-packages/rostest/*

%__ros_in_pkg tools/rostopic	rostopic
Requires:	ros-kinetic-genpy >= 0.5.4
Requires:	ros-kinetic-rosbag
Requires:	ros-kinetic-rospy
%__ros_in_files tools/rostopic	rostopic
%{__ros_install_path}/bin/rostopic
%{__ros_install_path}/lib/python2.7/site-packages/rostopic*
%{__ros_install_path}/lib/python2.7/site-packages/rostopic/*

%__ros_in_pkg tools/topic_tools	topic-tools
Requires:	ros-kinetic-message-runtime
Requires:	ros-kinetic-rosconsole
Requires:	ros-kinetic-roscpp
Requires:	ros-kinetic-rostime
Requires:	ros-kinetic-std-msgs
Requires:	ros-kinetic-xmlrpcpp
%__ros_in_files tools/topic_tools	topic-tools
%{__ros_install_path}/lib/python2.7/site-packages/topic_tools*
%{__ros_install_path}/lib/python2.7/site-packages/topic_tools/*

%__ros_in_pkg utilities/message_filters	message-filters
Requires:	ros-kinetic-rosconsole
Requires:	ros-kinetic-roscpp
Requires:	ros-kinetic-xmlrpcpp
%__ros_in_files utilities/message_filters	message-filters
%{__ros_install_path}/lib/python2.7/site-packages/message_filters*
%{__ros_install_path}/lib/python2.7/site-packages/message_filters/*

%__ros_in_pkg utilities/roslz4	roslz4
Requires:	lz4
%__ros_in_files utilities/roslz4	roslz4
%{__ros_install_path}/lib/python2.7/site-packages/roslz4*
%{__ros_install_path}/lib/python2.7/site-packages/roslz4/*

%__ros_in_pkg utilities/roswtf	roswtf
Requires:	python-paramiko
Requires:	python-rospkg
Requires:	ros-kinetic-rosbuild
Requires:	ros-kinetic-rosgraph
Requires:	ros-kinetic-roslaunch
Requires:	ros-kinetic-roslib
Requires:	ros-kinetic-rosnode
Requires:	ros-kinetic-rosservice
%__ros_in_files utilities/roswtf	roswtf
%{__ros_install_path}/bin/roswtf
%{__ros_install_path}/lib/python2.7/site-packages/roswtf*
%{__ros_install_path}/lib/python2.7/site-packages/roswtf/*

%__ros_in_pkg utilities/xmlrpcpp	xmlrpcpp
Requires:	ros-kinetic-cpp-common
%__ros_in_files utilities/xmlrpcpp	xmlrpcpp

%changelog
* Fri Oct 20 2017 MyungJoo Ham <myungjoo-ham@samsung.com> - 1.13.2
- Added RPM spec file
