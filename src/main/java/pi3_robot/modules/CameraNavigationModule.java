package pi3_robot.modules;

import java.util.concurrent.Semaphore;

import org.ros.exception.RemoteException;
import org.ros.exception.ServiceNotFoundException;
import org.ros.node.ConnectedNode;
import org.ros.node.service.ServiceClient;
import org.ros.node.service.ServiceResponseListener;
import org.ros.node.topic.Publisher;
import org.ros.node.topic.Subscriber;

import pi3_robot_2019.RunFunction;
import std_msgs.Int32;
import std_srvs.Empty;
import std_srvs.EmptyRequest;
import std_srvs.EmptyResponse;



public class CameraNavigationModule {
	
	String robotId;
	
	int last_command_performed = -1;
	
	private Publisher<Int32> command_publisher;
	private Subscriber<Int32> last_command_listener; 
	private ServiceClient<EmptyRequest, EmptyResponse> reset_commands_client = null;
	
	public CameraNavigationModule(String robotId, ConnectedNode node) {
		// TODO Auto-generated constructor stub
		this.robotId = robotId; 
		var remote_node_name = "/pi3_robot_2019/" + robotId + "/camera_navigator";
		try {
			reset_commands_client = node.newServiceClient(remote_node_name + "/reset_command", Empty._TYPE);
		} catch (ServiceNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			System.out.println("ERROR: service '"+ remote_node_name + "/reset_command" +"' not found");
			System.exit(-1);
		}
		
		command_publisher = node.newPublisher(remote_node_name + "/commands" , Int32._TYPE);
		command_publisher.setLatchMode(true);
		
		last_command_listener = node.newSubscriber(remote_node_name + "/last_destination", Int32._TYPE);
		last_command_listener.addMessageListener( message -> setLastCommandPerformed(message.getData()), 1);
		
	}
	
	synchronized private void setLastCommandPerformed(int value) {
		// System.out.println("Setting Last command: " + value);
		last_command_performed = value;
	}
	
	synchronized public int getLastCommandPerformed() {
		System.out.println("last performed: " + last_command_performed);
		return last_command_performed;
	}
	
	public void send_command(int command_id) {
		var msg = command_publisher.newMessage();
		msg.setData(command_id);
		command_publisher.publish(msg);
	}
	
	Semaphore waitSuccess = new Semaphore(0);
	public void reset_commads() {
		EmptyRequest request = reset_commands_client.newMessage();
		reset_commands_client.call(request, new ServiceResponseListener<EmptyResponse>() {
			
			@Override
			public void onSuccess(EmptyResponse arg0) {
				// TODO Auto-generated method stub
				waitSuccess.release();
			}
			
			@Override
			public void onFailure(RemoteException arg0) {
				// TODO Auto-generated method stub
				System.err.println("ERROR: pi3 robot could not reset commands, module might not be running");
				System.exit(-1);
			}
		});
		try {
			waitSuccess.acquire();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	
}
