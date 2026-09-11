package src.java;

import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.mapreduce.Reducer;

public class StudentReducer
        extends Reducer<Text, DoubleWritable, Text, DoubleWritable> {

    private DoubleWritable result = new DoubleWritable();

    public void reduce(Text key,
                       Iterable<DoubleWritable> values,
                       Context context)
            throws IOException, InterruptedException {

        double sum = 0;
        int count = 0;

        // Calculate total score
        for (DoubleWritable value : values) {
            sum += value.get();
            count++;
        }

        // Calculate average
        double average = sum / count;

        result.set(average);

        context.write(key, result);
    }
}