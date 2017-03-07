/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package smartlighting;

import org.wso2.siddhi.core.ExecutionPlanRuntime;
import org.wso2.siddhi.core.SiddhiManager;
import org.wso2.siddhi.core.event.Event;
import org.wso2.siddhi.core.query.output.callback.QueryCallback;
import org.wso2.siddhi.core.stream.input.InputHandler;
import org.wso2.siddhi.core.util.EventPrinter;
/**
 *
 * @author bernardo
 */
public class Test {
    /*public static void main(String[] args) throws InterruptedException {

        // Creating Siddhi Manager
        SiddhiManager siddhiManager = new SiddhiManager();

        String executionPlan = "" +
                "define stream cseEventStream (symbol string, price float, volume long); " +
                "" +
                "@info(name = 'query1') " +
                "from cseEventStream[volume < 150] " +
                "select symbol,price " +
                "insert into outputStream ;";

        //Generating runtime
        ExecutionPlanRuntime executionPlanRuntime = siddhiManager.createExecutionPlanRuntime(executionPlan);

        //Adding callback to retrieve output events from query
        executionPlanRuntime.addCallback("query1", new QueryCallback() {
            @Override
            public void receive(long timeStamp, Event[] inEvents, Event[] removeEvents) {
                EventPrinter.print(timeStamp, inEvents, removeEvents);
            }
        });

        //Retrieving InputHandler to push events into Siddhi
        InputHandler inputHandler = executionPlanRuntime.getInputHandler("cseEventStream");

        //Starting event processing
        executionPlanRuntime.start();

        //Sending events to Siddhi
        inputHandler.send(new Object[]{"IBM", 700f, 100l});
        inputHandler.send(new Object[]{"WSO2", 60.5f, 200l});
        inputHandler.send(new Object[]{"GOOG", 50f, 30l});
        inputHandler.send(new Object[]{"IBM", 76.6f, 400l});
        inputHandler.send(new Object[]{"WSO2", 45.6f, 50l});
        Thread.sleep(500);

        //Shutting down the runtime
        executionPlanRuntime.shutdown();

        //Shutting down Siddhi
        siddhiManager.shutdown();

    }*/
}
