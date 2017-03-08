/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package smartlighting;

import smartlighting.Resources.Event;

import com.google.gson.Gson;
import java.util.ArrayList;
import java.util.regex.Pattern;
import javafx.util.Pair;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import smartlighting.CEP.ExecutionPlan;
import redis.clients.jedis.Jedis; 
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;
import smartlighting.Resources.Adapters;


public class MQTTClient implements MqttCallback {

    MqttClient client;
    Adapters adapters;
    

    public static void main(String[] args) {
        
        ExecutionPlan plan = new ExecutionPlan(
                "define stream in_events_IT2_floor_0_Sala_1_1_all_3301_all_5700_all (device string, object int, object_instance int, resource int, resource_instance int, value float);\n" +
                "\n" +
                "define stream out_events_IT2_floor_0_Sala_1_1_all_1501_all_15012_all (meta_operation string, value int);\n" +
                "\n" +
                "define stream in_events_IT2_floor_0_Sala_1_2_all_3301_all_5700_all (device string, object int, object_instance int, resource int, resource_instance int, value float);\n" +
                "\n" +
                "define stream out_events_IT2_floor_0_Sala_1_2_all_1501_all_15012_all (meta_operation string, value int);\n" +
                "\n" +
                "from in_events_IT2_floor_0_Sala_1_1_all_3301_all_5700_all\n" +
                "select 'set' as meta_operation, convert( ( 100 -(value * 3.333333) ) , 'int') as value\n" +
                "insert into out_events_IT2_floor_0_Sala_1_1_all_1501_all_15012_all;\n" +
                "\n" +
                "from in_events_IT2_floor_0_Sala_1_2_all_3301_all_5700_all\n" +
                "select 'set' as meta_operation, convert( ( 100 -(value * 3.333333) ) , 'int') as value\n" +
                "insert into out_events_IT2_floor_0_Sala_1_2_all_1501_all_15012_all;", 
                "{\"name\":\"Teste\",\"subrules\":[{\"actions\":[{\"target\":{\"type\":\"mqtt\",\"topic\":\"\\/out_events\\/IT2\\/floor_0\\/Sala\\/1\\/1\\/all\\/1501\\/all\\/15011\\/all\",\"value_type\":\"int\"},\"function\":{\"name\":\"set_value\",\"listen_data\":{\"type\":\"single\",\"listeners\":[{\"type\":\"mqtt\",\"topic\":\"\\/in_events\\/IT2\\/floor_0\\/Sala\\/1\\/1\\/+\\/3302\\/+\\/5500\\/+\",\"value_type\":\"int\"}],\"window\":{\"type\":\"time\",\"value\":4,\"units\":\"seconds\"},\"aggregator\":{\"type\":\"any\"}}}}]},{\"actions\":[{\"target\":{\"type\":\"mqtt\",\"topic\":\"\\/out_events\\/IT2\\/floor_0\\/Sala\\/1\\/2\\/all\\/1501\\/all\\/15011\\/all\",\"value_type\":\"int\"},\"function\":{\"name\":\"set_value\",\"listen_data\":{\"type\":\"single\",\"listeners\":[{\"type\":\"mqtt\",\"topic\":\"\\/in_events\\/IT2\\/floor_0\\/Sala\\/1\\/2\\/+\\/3302\\/+\\/5500\\/+\",\"value_type\":\"int\"}],\"window\":{\"type\":\"time\",\"value\":4,\"units\":\"seconds\"},\"aggregator\":{\"type\":\"any\"}}}}]}]}");
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
            if(((Pattern)i).matcher(topic).matches()){
                System.out.println("BELONGS");
            }
        }
        
        Event inEvent = new Gson().fromJson(message.toString(), Event.class);
        System.out.println(inEvent.getEvent().getPayloadData().getDevice());
        
    }

    @Override
    public void deliveryComplete(IMqttDeliveryToken token) {
        // TODO Auto-generated method stub

    }

}