package pi3_robot_2019;

public interface RunFunctionRequest extends org.ros.internal.message.Message {
  static final java.lang.String _TYPE = "pi3_robot_2019/RunFunctionRequest";
  static final java.lang.String _DEFINITION = "string function_id\nstring[] params\n";
  java.lang.String getFunctionId();
  void setFunctionId(java.lang.String value);
  java.util.List<java.lang.String> getParams();
  void setParams(java.util.List<java.lang.String> value);
}
