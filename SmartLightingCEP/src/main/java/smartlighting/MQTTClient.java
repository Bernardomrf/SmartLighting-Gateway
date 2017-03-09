/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package smartlighting;

import smartlighting.Resources.Event;

import com.google.gson.Gson;
import java.util.ArrayList;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.regex.Pattern;
import javafx.util.Pair;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.wso2.siddhi.core.ExecutionPlanRuntime;
import org.wso2.siddhi.core.SiddhiManager;
import org.wso2.siddhi.core.query.output.callback.QueryCallback;
import org.wso2.siddhi.core.stream.input.InputHandler;
import org.wso2.siddhi.core.util.EventPrinter;
import smartlighting.CEP.ExecutionP;
import redis.clients.jedis.Jedis; 
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;
import smartlighting.Resources.Adapters;


public class MQTTClient implements MqttCallback {

    MqttClient client;
    Adapters adapters;
    static SiddhiManager siddhiManager; 
    static ExecutionPlanRuntime executionPlanRuntime;

    public static void main(String[] args) {
        
        siddhiManager = new SiddhiManager();
        ExecutionP plan = new ExecutionP(
                
                "define stream in_events_IT2_floor_0_Sala_1_1_all_3301_all_5700_all (device string, object int, object_instance int, resource int, resource_instance int, value float);\n" +
                "\n" +
                "define stream out_events_IT2_floor_0_Sala_1_1_all_1501_all_15012_all (meta_operation string, value int);\n" +
                "\n" +
                "define stream in_events_IT2_floor_0_Sala_1_2_all_3301_all_5700_all (device string, object int, object_instance int, resource int, resource_instance int, value float);\n" +
                "\n" +
                "define stream out_events_IT2_floor_0_Sala_1_2_all_1501_all_15012_all (meta_operation string, value int);\n" +
                "\n" +
                "@info(name = 'query1') " +
                "from in_events_IT2_floor_0_Sala_1_1_all_3301_all_5700_all\n" +
                "select 'set' as meta_operation, convert( ( 100 -(value * 3.333333) ) , 'int') as value\n" +
                "insert into out_events_IT2_floor_0_Sala_1_1_all_1501_all_15012_all;\n" +
                "\n" +
                "@info(name = 'query2') " +
                "from in_events_IT2_floor_0_Sala_1_2_all_3301_all_5700_all\n" +
                "select 'set' as meta_operation, convert( ( 100 -(value * 3.333333) ) , 'int') as value\n" +
                "insert into out_events_IT2_floor_0_Sala_1_2_all_1501_all_15012_all;", 
                "{\"name\":\"Lights\",\"subrules\":[{\"actions\":[{\"target\":{\"type\":\"mqtt\",\"topic\":\"\\/out_events\\/IT2\\/floor_0\\/Sala\\/1\\/1\\/all\\/1501\\/all\\/15012\\/all\",\"value_type\":\"integer\"},\"function\":{\"name\":\"set_value\",\"listen_data\":{\"type\":\"single\",\"listeners\":[{\"type\":\"mqtt\",\"topic\":\"\\/in_events\\/IT2\\/floor_0\\/Sala\\/1\\/1\\/+\\/3301\\/+\\/5700\\/+\",\"value_type\":\"float\"}],\"converter\":{\"type\":\"lux_to_percentage\",\"max_lux\":30.0}}}}]},{\"actions\":[{\"target\":{\"type\":\"mqtt\",\"topic\":\"\\/out_events\\/IT2\\/floor_0\\/Sala\\/1\\/2\\/all\\/1501\\/all\\/15012\\/all\",\"value_type\":\"integer\"},\"function\":{\"name\":\"set_value\",\"listen_data\":{\"type\":\"single\",\"listeners\":[{\"type\":\"mqtt\",\"topic\":\"\\/in_events\\/IT2\\/floor_0\\/Sala\\/1\\/2\\/+\\/3301\\/+\\/5700\\/+\",\"value_type\":\"float\"}],\"converter\":{\"type\":\"lux_to_percentage\",\"max_lux\":30.0}}}}]}]}");
        //Generating runtime
        executionPlanRuntime = siddhiManager.createExecutionPlanRuntime(plan.getEP());

        //Adding callback to retrieve output events from query
        executionPlanRuntime.addCallback("query1", new QueryCallback() {
            @Override
            public void receive(long timeStamp, org.wso2.siddhi.core.event.Event[] inEvents, org.wso2.siddhi.core.event.Event[] removeEvents) {
                EventPrinter.print(timeStamp, inEvents, removeEvents);
                if(inEvents!=null){
                    System.out.println(inEvents[0].getData()[0].toString());
                    System.out.println(inEvents[0].getData()[1].toString());
                }
            }
        });
        executionPlanRuntime.addCallback("query2", new QueryCallback() {
            @Override
            public void receive(long timeStamp, org.wso2.siddhi.core.event.Event[] inEvents, org.wso2.siddhi.core.event.Event[] removeEvents) {
                EventPrinter.print(timeStamp, inEvents, removeEvents);
                System.out.println("2");
            }
        });

        //Starting event processing
        executionPlanRuntime.start();
        
        
        new MQTTClient().initClient();
    }

    public void initClient() {
        try {
            adapters = new Adapters();
            
            client = new MqttClient("tcp://localhost:1883", "Sending");
            client.connect();
            client.setCallback(this);
            client.subscribe("/SM/in_events/IT2/floor_0/#");

        } catch (MqttException e) {
            System.err.println("Erro: "+ e.toString());
        }
    }

    @Override
    public void connectionLost(Throwable cause) {
        // TODO Auto-generated method stub

    }

    @Override
    public void messageArrived(String topic, MqttMessage message)
            throws Exception {

        //System.out.println(tmp);
        for(Object i : (ArrayList) adapters.getAdapters("receiver")){
            if(((Pattern)((Pair<Object, String>)i).getKey()).matcher(topic).matches()){
                System.out.println("BELONGS");
                System.out.println(topic);
                Event inEvent = new Gson().fromJson(message.toString(), Event.class);
                //System.out.println((String)((Pair<Object, String>)i).getValue());
                //Retrieving InputHandler to push events into Siddhi  object_instance int, resource int, resource_instance int, value int
                InputHandler inputHandler = executionPlanRuntime.getInputHandler((String)((Pair<Object, String>)i).getValue());
                try {
                    inputHandler.send(new Object[]{inEvent.getEvent().getPayloadData().getDevice(), 
                                                   inEvent.getEvent().getPayloadData().getObject(), 
                                                   inEvent.getEvent().getPayloadData().getObject_instance(), 
                                                   inEvent.getEvent().getPayloadData().getResource(),
                                                   inEvent.getEvent().getPayloadData().getResource_instance(),
                                                   inEvent.getEvent().getPayloadData().getValue()});
                } catch (InterruptedException ex) {
                    System.out.println("ERRO");
                }
            }
        }
            
    }

    @Override
    public void deliveryComplete(IMqttDeliveryToken token) {
        // TODO Auto-generated method stub

    }

}