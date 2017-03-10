/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package smartlighting.mqtt;

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
import org.wso2.siddhi.core.stream.input.InputHandler;
import smartlighting.CEP.MessageManager;
import smartlighting.Resources.Event;

/**
 *
 * @author bernardo
 */
public class MqttListener extends Thread {
    
    private String host, topic;
    private MessageManager messageManager; 
    
    public MqttListener(String host, String topic){
        this.host = host;
        this.topic = topic;
        this.messageManager = new MessageManager();
    }
    
    @Override
    public void run(){
        try {
            MqttClient client;
            
            client = new MqttClient(host, MqttClient.generateClientId());
            client.connect();
            client.subscribe(topic);
            client.setCallback(new MqttCallback() {
                
                @Override
                public void connectionLost(Throwable thrwbl) {
                    throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
                }

                @Override
                public void messageArrived(String topic, MqttMessage message) throws Exception {
                    messageManager.newMessage(topic, message);
                }

                @Override
                public void deliveryComplete(IMqttDeliveryToken imdt) {
                    throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
                }
            });
            
            
        } catch (MqttException ex) {
            Logger.getLogger(MqttListener.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
}
