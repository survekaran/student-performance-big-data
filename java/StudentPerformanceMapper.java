package studentperformance;

import java.io.IOException;

import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class StudentPerformanceMapper
        extends Mapper<Object, Text, Text, DoubleWritable> {

    private final Text school = new Text();
    private final DoubleWritable grade = new DoubleWritable();

    @Override
    public void map(Object key, Text value, Context context)
            throws IOException, InterruptedException {

        String line = value.toString();

        // Skip CSV header
        if (line.startsWith("school;")) {
            return;
        }

        String[] fields = line.split(";");

        // G3 is column 33 (index 32)
        // school is column 1 (index 0)
        if (fields.length >= 33) {
            try {
                String schoolValue = fields[0].replace("\"", "").trim();
                String g3Value = fields[32].replace("\"", "").trim();

                double g3 = Double.parseDouble(g3Value);

                school.set(schoolValue);
                grade.set(g3);

                context.write(school, grade);

            } catch (NumberFormatException e) {
                // Ignore invalid rows
            }
        }
    }
}
