# Check if CSV file exists; if not, create it
csv_file_exist <- function(file_path, data_to_write) {
  # Check if the file exists
  if (file.exists(file_path)) {
    cat("The CSV file at", file_path, "already exists.\n")
  } else {
    # The file does not exist, create it
    cat("The CSV file at", file_path, "does not exist. Creating the file...\n")
    write.csv2(data_to_write, file = file_path, row.names = FALSE, quote = FALSE)
    cat("CSV file created at", file_path, "\n")
  }
}
