/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package smartlighting;

import smartlighting.mqtt.MqttListener;

/**
 *
 * @author bernardo
 */
public class GatewayCEP {
    public static void main(String[] args){
        
        String HOST = "tcp://localhost:1883";
        String TOPIC = "/SM/in_events/IT2/floor_0/#";
        
        MqttListener list = new MqttListener(HOST, TOPIC);
        list.start();
    }
}
