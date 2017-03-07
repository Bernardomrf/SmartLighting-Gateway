/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package smartlighting.Resources;

/**
 *
 * @author bernardo
 */
public class Event {
    private PayloadData event;
    
    public PayloadData getEvent(){
        return event;
    }

    /**
     * @param event the event to set
     */
    public void setEvent(PayloadData event) {
        this.event = event;
    }
}
