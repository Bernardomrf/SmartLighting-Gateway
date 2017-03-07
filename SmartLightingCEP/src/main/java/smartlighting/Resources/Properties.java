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
public class Properties {
    
    private String device;
    private int object;
    private int object_instance;
    private int resource;
    private int resource_instance;
    private float value;
    
    public String getDevice(){
        return device;
    }

    /**
     * @param device the device to set
     */
    public void setDevice(String device) {
        this.device = device;
    }

    /**
     * @return the object
     */
    public int getObject() {
        return object;
    }

    /**
     * @param object the object to set
     */
    public void setObject(int object) {
        this.object = object;
    }

    /**
     * @return the object_instance
     */
    public int getObject_instance() {
        return object_instance;
    }

    /**
     * @param object_instance the object_instance to set
     */
    public void setObject_instance(int object_instance) {
        this.object_instance = object_instance;
    }

    /**
     * @return the resource
     */
    public int getResource() {
        return resource;
    }

    /**
     * @param resource the resource to set
     */
    public void setResource(int resource) {
        this.resource = resource;
    }

    /**
     * @return the resource_instance
     */
    public int getResource_instance() {
        return resource_instance;
    }

    /**
     * @param resource_instance the resource_instance to set
     */
    public void setResource_instance(int resource_instance) {
        this.resource_instance = resource_instance;
    }

    /**
     * @return the value
     */
    public float getValue() {
        return value;
    }

    /**
     * @param value the value to set
     */
    public void setValue(float value) {
        this.value = value;
    }
}
