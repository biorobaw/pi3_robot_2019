package pi3_robot;
import java.net.URI;
import java.util.HashMap;
import java.util.concurrent.Semaphore;

import org.ros.internal.loader.CommandLineLoader;
import org.ros.namespace.GraphName;
import org.ros.node.AbstractNodeMain;
import org.ros.node.ConnectedNode;
import org.ros.node.DefaultNodeMainExecutor;
import org.ros.node.Node;
import org.ros.node.NodeConfiguration;
import org.ros.node.NodeMainExecutor;
import org.ros.node.topic.Publisher;

import com.google.common.collect.Lists;


public class Pi3Robot extends AbstractNodeMain  {
	
	static HashMap<String, Pi3Robot> robots = new HashMap<String, Pi3Robot>();
	static public Pi3Robot getRobot(String id) {
		return robots.get(id);
	}
	enum TopicList {speed_cmd }
	
	
	
	String robotId;
	String rosMasterIp;
	String rosMasterPort;
	Publisher<geometry_msgs.Twist> speed_publisher;
	
	
	Semaphore waitNodeStarted = new Semaphore(0);
	
	
	public Pi3Robot(String robotId, String ip, String port) {
		// TODO Auto-generated constructor stub
		if(robots.containsKey(robotId)) {
			System.out.println("ERROR: robot with id " + robotId + " already exits");
			System.exit(-1);
		}

		this.robotId = robotId;
		rosMasterIp = ip;
		rosMasterPort = port;
		
		robots.put(robotId, this);		
		
		
		var args = Lists.newArrayList(new String[] {"ROS_IP="+ip});
		CommandLineLoader loader = new CommandLineLoader(args); 
//		NodeConfiguration nodeConfiguration = loader.build() ;
		NodeConfiguration nodeConfiguration = NodeConfiguration.newPublic(ip);
		nodeConfiguration.setMasterUri(URI.create("http://"+ip+":" + port));

		
		NodeMainExecutor nodeMainExecutor = DefaultNodeMainExecutor.newDefault();
		nodeMainExecutor.execute(this, nodeConfiguration);
		
		try {
			System.out.println("Pi3Robot: Waiting for ROS node to start");
			waitNodeStarted.acquire();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			System.err.println("ERROR: ROS Pi3Robot never started");
			System.exit(-1);
		}
		
	}
	
	
	public GraphName getDefaultNodeName() {
		// TODO Auto-generated method stub
		return GraphName.of("pi3_robot_2019_proxy/"+robotId);
	}
	
	
	
	
	
	@Override
	public void onStart(ConnectedNode connectedNode) {
		// TODO Auto-generated method stub
		super.onStart(connectedNode);
		
		speed_publisher = connectedNode.newPublisher("/" +robotId + "/" + TopicList.speed_cmd, geometry_msgs.Twist._TYPE);

		
		
		System.out.println("Node sarted, releasing lock");
		waitNodeStarted.release();
	}
	
	@Override
	public void onShutdown(Node node) {
		// TODO Auto-generated method stub
		super.onShutdown(node);
//		System.out.println("Pi3Robot: SHUTTING DOWN");
	}

	synchronized public void setSpeed(float v, float w) {
		var msg = speed_publisher.newMessage();
		msg.getAngular().setZ(w);
		msg.getLinear().setX(v);
		speed_publisher.publish(msg);
	}
	

	

	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		String rosMasterIp = "10.226.14.37";
		String port = "11311";
		Pi3Robot robot = new Pi3Robot("b1", rosMasterIp, port);
		int i = 0;
		while(true) {
			robot.setSpeed((float)0.0, 0);
			i = (i+1)%10;
//			System.out.println("sending "+i);
			try {
				Thread.sleep(100);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}

	}
	
}
