/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package smartlighting;

import smartlighting.Resources.Event;

import com.google.gson.Gson;
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
    Adapters redis;

    public static void main(String[] args) {
        
        ExecutionPlan plan = new ExecutionPlan("","{\"name\":\"Teste\",\"subrules\":[{\"actions\":[{\"target\":{\"type\":\"mqtt\",\"topic\":\"\\/out_events\\/IT2\\/floor_0\\/Sala\\/1\\/1\\/all\\/1501\\/all\\/15011\\/all\",\"value_type\":\"int\"},\"function\":{\"name\":\"set_value\",\"listen_data\":{\"type\":\"single\",\"listeners\":[{\"type\":\"mqtt\",\"topic\":\"\\/in_events\\/IT2\\/floor_0\\/Sala\\/1\\/1\\/+\\/3302\\/+\\/5500\\/+\",\"value_type\":\"int\"}],\"window\":{\"type\":\"time\",\"value\":4,\"units\":\"seconds\"},\"aggregator\":{\"type\":\"any\"}}}}]},{\"actions\":[{\"target\":{\"type\":\"mqtt\",\"topic\":\"\\/out_events\\/IT2\\/floor_0\\/Sala\\/1\\/2\\/all\\/1501\\/all\\/15011\\/all\",\"value_type\":\"int\"},\"function\":{\"name\":\"set_value\",\"listen_data\":{\"type\":\"single\",\"listeners\":[{\"type\":\"mqtt\",\"topic\":\"\\/in_events\\/IT2\\/floor_0\\/Sala\\/1\\/2\\/+\\/3302\\/+\\/5500\\/+\",\"value_type\":\"int\"}],\"window\":{\"type\":\"time\",\"value\":4,\"units\":\"seconds\"},\"aggregator\":{\"type\":\"any\"}}}}]}]}");
        //new MQTTClient().initClient();
    }

    public void initClient() {
        try {
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
        System.out.println(topic);
        //System.out.println(message);   
        Event inEvent = new Gson().fromJson(message.toString(), Event.class);
        System.out.println(inEvent.getEvent().getPayloadData().getDevice());
        
    }

    @Override
    public void deliveryComplete(IMqttDeliveryToken token) {
        // TODO Auto-generated method stub

    }

}