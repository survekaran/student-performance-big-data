package src.java;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class StudentDriver {

    public static void main(String[] args) throws Exception {

        // Create Hadoop configuration
        Configuration conf = new Configuration();

        // Create MapReduce job
        Job job = Job.getInstance(conf, "Student Performance Analysis");

        // Set main class
        job.setJarByClass(StudentDriver.class);

        // Set Mapper
        job.setMapperClass(StudentMapper.class);

        // Set Reducer
        job.setReducerClass(StudentReducer.class);

        // Mapper output types
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(DoubleWritable.class);

        // Final output types
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(DoubleWritable.class);

        // Input and Output paths
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        // Run the job
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}