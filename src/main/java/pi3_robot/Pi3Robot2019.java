package pi3_robot;

import java.net.Inet4Address;
import java.net.URI;
import java.util.HashMap;
import java.util.Scanner;

import org.opencv.core.Mat;
import org.opencv.core.MatOfByte;
import org.opencv.imgcodecs.Imgcodecs;
import org.ros.exception.RemoteException;
import org.ros.exception.ServiceNotFoundException;
import org.ros.message.Time;
import org.ros.namespace.GraphName;
import org.ros.node.AbstractNodeMain;
import org.ros.node.ConnectedNode;
import org.ros.node.DefaultNodeMainExecutor;
import org.ros.node.Node;
import org.ros.node.NodeConfiguration;
import org.ros.node.NodeMainExecutor;
import org.ros.node.service.ServiceClient;
import org.ros.node.service.ServiceResponseListener;
import org.ros.node.topic.Publisher;
import org.ros.node.topic.Subscriber;

import pi3_robot.modules.CameraNavigationModule;
import pi3_robot_2019.RunFunction;
import pi3_robot_2019.RunFunctionRequest;
import pi3_robot_2019.RunFunctionResponse;
import sensor_msgs.CompressedImage;
import std_msgs.Float32MultiArray;;

/**
 * Class to control the lab's robot pi3_robot from 2019
 * 
 * @author bucef
 *
 */
public class Pi3Robot2019 extends AbstractNodeMain {

	// =========================================================================================
	// ============================ CONTROLLER TEST FUNCTION ===================================
	// =========================================================================================

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		// variables to setup connection
		String rosMasterHostname = "LAPTOP-J2CEGRMV"; // hostname instead of ip
		rosMasterHostname = "rpi2019";
		String robotId = "r1";	// id of robot, has to match the one in the robot drivers folder
		
		// create instace of the robot
		// the robot initializes only with basic functionality
		Pi3Robot2019 robot = new Pi3Robot2019(robotId, rosMasterHostname);
		
		// add desired modules
		robot.initDistanceSensors(true);
		robot.initCamera(true);
		var navigationModule = robot.initCameraNavigationModule();
		
		// test camera module
//		var frame = robot.getLatestFrame();
//		Imgcodecs.imwrite("D:\\Desktop\\img.jpg", frame.frame);
		
		
		Scanner in = new Scanner(System.in); 
		
		// test set speeds and distance sensing modules
		int i = 0;
		while (true) {
//			var d = robot.getDistance();
//			System.out.println("distances: " +d[0] + "," + d[1]+ " " + d[2] );
//			robot.setSpeed((float) 0.0, 0);
//			i = (i + 1) % 10;
////					System.out.println("sending "+i);
			
			System.out.println();
			System.out.print("Enter command:");
			var cmd = in.nextLine();
			var tokens = cmd.split(" ");
			
			switch(tokens[0]) {
			
				case "feeder":
					if (tokens.length > 1) {
						var next_command = Integer.parseInt(tokens[1]);
						navigationModule.send_command(next_command);
						while(navigationModule.getLastCommandPerformed()!=next_command)
							wait(100);
					}
					break;
				case "reset":
					navigationModule.reset_commads();
					break;
				case "exit":
					System.out.println("exit successful!");
					System.exit(0);
			
			}
			
			wait(100);
			
			
			
		}

	}
	
	static void wait(int ms) {
		try {
			Thread.sleep(ms);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	// =========================================================================================
	// ============================ PUBLIC API =================================================
	// =========================================================================================

	/**
	 * Controller constructor
	 * 
	 * @param id          id of the robot (must match the robot's id)
	 * @param rosHostname hostname of the node running roscore
	 */
	public Pi3Robot2019(String id, String rosHostname) {
		this(id, rosHostname, "11311");
	}

	/**
	 * Controller constructor
	 * 
	 * @param id            id of the robot (must match the robot's id)
	 * @param rosHostname   hostname of the node running roscore
	 * @param masterPort 	port of the roscore process (default is 11311)
	 */
	public Pi3Robot2019(String id, String rosHostname, String masterPort) {

		// verify the controller does not yet exist
		synchronized (Pi3Robot2019.class) {
			if (robots.containsKey(id)) {
				System.err.println("ERROR: robot with id '" + id + "' already exists");
				new Exception().printStackTrace();
				System.exit(-1);
			} else {
				this.robotId = id;
				robots.put(id, this);
			}
		}

		// proceed to create the controller
		createControllerNode(rosHostname, masterPort);
	}

	/**
	 * Static function to get the robot controller belonging to the corresponding id
	 * 
	 * @param id
	 * @return
	 */
	static synchronized public Pi3Robot2019 getRobot(String id) {

		return robots.get(id);
	}

	/**
	 * Subscribes to the robot camera publisher
	 * 
	 * @param block Indicates whether to block until frames are received
	 */
	public void initCamera(boolean block) {
		subscribeToCamera("/pi3_robot_2019/" + robotId + "/cam/image/compressed", block);
	}

	/**
	 * Get the latest frame from the camera
	 * 
	 * @return returns a class containing an opencv frame and a time stamp
	 */
	public MyFrame getLatestFrame() {
		return latestFrame;
	}

	/**
	 * Sets the desired linear and angular speeds of the robot.
	 * 
	 * @param linear  linear speed in meters per second
	 * @param angular angular speed in radians per second
	 */
	synchronized public void setSpeed(float linear, float angular) {
		var msg = speed_vw_publisher.newMessage();
		msg.getAngular().setZ(angular);
		msg.getLinear().setX(linear);
		speed_vw_publisher.publish(msg);
	}

	/**
	 * Subscribes to the robot sensor messages
	 * @param block indicates whether to block until packages are
	 */
	void initDistanceSensors(boolean block) {
		subscribeToDistanceSensor("/pi3_robot_2019/" + robotId + "/distance_sensors/d_data", block);
	}
	
	
	/**
	 * Returns an array containing the distances measured by the sensors (left,
	 * front, right)
	 * 
	 * @return
	 */
	public float[] getDistance() {
		return distanceSensorData;
	}

	/**
	 * initialzes the camera navigation module
	 */
	public CameraNavigationModule initCameraNavigationModule() {
		if(cameraNavigationModule == null)
			cameraNavigationModule = new CameraNavigationModule(robotId, connectedNode);
		return cameraNavigationModule;
	}
	
	public CameraNavigationModule getCameraNavigationModule() {
		return cameraNavigationModule;
	}
	
	
	
	// =========================================================================================
	// ============================ PRIVATE FIELD AND METHODS ==================================
	// =========================================================================================

	// ROBOT ID AND ROS CONNECTION VARIABLES
	String robotId;

	// HashMap containing the initialized robots
	static HashMap<String, Pi3Robot2019> robots = new HashMap<String, Pi3Robot2019>();

	// variables to hold the ros node along with subscribers and service clients
	ConnectedNode connectedNode = null;
	private ServiceClient<RunFunctionRequest, RunFunctionResponse> runFunctionClient = null;
	private Publisher<geometry_msgs.Twist> speed_vw_publisher;
	private CameraNavigationModule cameraNavigationModule = null;

	// ================ COMMUNICATION WITH ROS ===========================

	
	/**
	 * Return the name of the robot for defining ros node/topic names
	 */
	private String getRobotName() {
		return "/pi3_robot_2019/" + robotId;
	}
	
	/**
	 * Return the name of the node
	 */
	@Override
	public GraphName getDefaultNodeName() {
		// TODO Auto-generated method stub
		return GraphName.of(getRobotName() + "/java");
	}

	/**
	 * Initialize a ros node for the robot controller and initialize
	 * the servo controller and run function service client
	 * 
	 * @param ip   ip of machine running roscore
	 * @param port port of roscore process (default is 11311)
	 */
	private void createControllerNode(String masterHostname, String masterPort) {

		try {
			// init ros node
			System.out.println("Pi3Robot: initializing ros node...");
			NodeConfiguration nodeConfiguration = NodeConfiguration.newPublic(
													Inet4Address.getLocalHost().getHostName(), 
													new URI("http://"+masterHostname+":"+masterPort)
			);
			NodeMainExecutor nodeMainExecutor = DefaultNodeMainExecutor.newDefault();
			nodeMainExecutor.execute(this, nodeConfiguration);
			
			// wait until node is connected
			while (connectedNode == null) Thread.sleep(30);
			
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			System.exit(-1);
		}	
	}

	/**
	 * Call back function called when the ros node was initialized
	 */
	@Override
	public void onStart(ConnectedNode connectedNode) {
		super.onStart(connectedNode);
		
		try {
			
			System.out.print("Pi3Robot: starting run function client...");
			runFunctionClient = connectedNode.newServiceClient("/pi3_robot_2019/" + robotId + "/run_function", RunFunction._TYPE);
			System.out.println(" done.");
			System.out.print("Pi3Robot: starting run function client...");
			speed_vw_publisher = connectedNode.newPublisher("/pi3_robot_2019/" + robotId + "/speed_vw", geometry_msgs.Twist._TYPE);
			System.out.println(" done.");
			this.connectedNode = connectedNode;
			
		} catch (ServiceNotFoundException e) {
			// TODO Auto-generated catch block
			System.out.println();
			e.printStackTrace();
			System.err.println("ERROR: could not initialize pi3_robot_2019");
			System.exit(-1);
		}
		
	}

	/**
	 * Call back function called when node is closed
	 */
	@Override
	public void onShutdown(Node node) {
		super.onShutdown(node);
	}
	
	// ================== CAMERA SUBSCRIBER: ==============================

	// variable to hold the latest frame
	private MyFrame latestFrame = null;

	// static initialization of opencv
	{
		nu.pattern.OpenCV.loadLocally();
	}

	/**
	 * Subscribe to a compressed image topic
	 * 
	 * @param topic the compressed image topic to subscribe to
	 * @param block indicates whether to block until the connection to the published
	 *              is established
	 */
	private void subscribeToCamera(String topic, boolean block) {

		// Send command to start camera:
		RunFunctionRequest request = runFunctionClient.newMessage();
		request.setFunctionId("init_camera");
		runFunctionClient.call(request, new ServiceResponseListener<RunFunctionResponse>() {
			
			@Override
			public void onSuccess(RunFunctionResponse arg0) {
				// TODO Auto-generated method stub
				// do nothing
			}
			
			@Override
			public void onFailure(RemoteException arg0) {
				// TODO Auto-generated method stub
				System.err.println("ERROR: pi3 robot could not start the camera");
				System.err.println("received error: " +arg0.getMessage());
			}
		});
		
		// subscribe to the topic,
		Subscriber<CompressedImage> subscriber = connectedNode.newSubscriber(topic, CompressedImage._TYPE);
		subscriber.addMessageListener(message -> {
			Time time = message.getHeader().getStamp();

			var data = message.getData();
			int imageStart = data.arrayOffset();

			Mat compressedFrame = new MatOfByte(imageStart, data.array().length - imageStart, data.array());
			Mat frame = Imgcodecs.imdecode(compressedFrame, Imgcodecs.CV_LOAD_IMAGE_COLOR); // .clone()
			latestFrame = new MyFrame(frame, time);
		});

		// if block was set to true, wait until images are received.
		if (block) {
			System.out.println("Waiting to connect to robot camera...");
			while (latestFrame == null) {
				try {
					Thread.sleep(30);
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
			System.out.println("Connected to robot camera");
		}
	}

	// Class returned by getLatestFrame
	private final class MyFrame {
		public Mat frame;
		public Time time;

		MyFrame(Mat frame, Time time) {
			this.frame = frame;
			this.time = time;
		}

		public Mat getFrame() {
			return frame;
		}

		public Time getTime() {
			return time;
		}
	}	

	// ============== DISTANCE SENSOR CONTROLLER ===============================

	private float[] distanceSensorData = null;
	
	/**
	 * Create subscriber for distance sensor packages
	 * @param topic  indicates the name of the topic to subscribe to
	 * @param block	 indicates whether to block until packages are received.
	 */
	private void subscribeToDistanceSensor(String topic, boolean block) {
		
		// Send command to start sensing:
		RunFunctionRequest request = runFunctionClient.newMessage();
		request.setFunctionId("init_distance_sensors");
		runFunctionClient.call(request, new ServiceResponseListener<RunFunctionResponse>() {
			
			@Override
			public void onSuccess(RunFunctionResponse arg0) {
				// TODO Auto-generated method stub
				
			}
			
			@Override
			public void onFailure(RemoteException arg0) {
				// TODO Auto-generated method stub
				System.err.println("ERROR: pi3 robot could not start the distance sensors");
				System.err.println("received error: " +arg0.getMessage());
			}
		});
		
		// create subscriber
		Subscriber<Float32MultiArray> subscriber = connectedNode.newSubscriber(topic , Float32MultiArray._TYPE);
		subscriber.addMessageListener(message -> {
			distanceSensorData = message.getData();
			// System.out.println(distanceSensorData[0] + "," + distanceSensorData[1] + "," + distanceSensorData[2]);
		});
		if(block) {
			System.out.println("Pi3Robot2019: Waiting to establish connection to sensor data publisher");
			while(distanceSensorData==null) {
				try {
					Thread.sleep(30);
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
			System.out.println("Pi3Robot2019: Connected to sensor data publisher");
		}
	}
	
	
}
