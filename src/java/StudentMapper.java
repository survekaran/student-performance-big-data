package src.java;

import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.mapreduce.Mapper;

public class StudentMapper
        extends Mapper<Object, Text, Text, DoubleWritable> {

    private Text category = new Text();
    private DoubleWritable score = new DoubleWritable();

    public void map(Object key, Text value, Context context)
            throws IOException, InterruptedException {

        // Skip CSV header
        String line = value.toString();

        if (line.startsWith("student_id")) {
            return;
        }

        // Split CSV row
        String[] data = line.split(",");

        // Example:
        // student_id,attendance,study_hours,previous_score,
        // assignment_score,internal_marks,final_score

        if (data.length < 7) {
            return;
        }

        double finalScore = Double.parseDouble(data[6]);

        // Create performance category
        String performance;

        if (finalScore >= 80) {
            performance = "Excellent";
        } else if (finalScore >= 60) {
            performance = "Good";
        } else if (finalScore >= 40) {
            performance = "Average";
        } else {
            performance = "Poor";
        }

        category.set(performance);
        score.set(finalScore);

        // Send category and score to Reducer
        context.write(category, score);
    }
}