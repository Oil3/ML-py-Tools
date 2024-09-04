import Foundation

// Function to clean up filenames
func cleanFilename(_ filename: String) -> String {
    // Split the filename into name and extension
    let url = URL(fileURLWithPath: filename)
    let name = url.deletingPathExtension().lastPathComponent
    let ext = url.pathExtension
    
    // Replace spaces with underscores
    var cleanName = name.replacingOccurrences(of: " ", with: "_")
    
    // Remove special characters, keeping only letters, numbers, underscores, and dashes
    cleanName = cleanName.components(separatedBy: CharacterSet.alphanumerics.inverted.union(CharacterSet(charactersIn: "_-"))).joined()
    
    // Ensure there is only one dot before the extension
    return "\(cleanName).\(ext)"
}

// Function to rename files in a directory and log the changes
func renameFiles(in directory: String) {
    let fileManager = FileManager.default
    let logFilePath = (directory as NSString).appendingPathComponent("rename_log.txt")
    
    // Create or overwrite the log file
    fileManager.createFile(atPath: logFilePath, contents: nil, attributes: nil)
    let logFile = FileHandle(forWritingAtPath: logFilePath)
    
    do {
        // Get the list of files in the directory
        let files = try fileManager.contentsOfDirectory(atPath: directory)
        
        for file in files {
            let filePath = (directory as NSString).appendingPathComponent(file)
            var isDir: ObjCBool = false
            
            // Check if the file is a directory
            if fileManager.fileExists(atPath: filePath, isDirectory: &isDir) && !isDir.boolValue {
                let newFilename = cleanFilename(file)
                let newFilePath = (directory as NSString).appendingPathComponent(newFilename)
                
                // Rename the file if the new name is different
                if file != newFilename {
                    try fileManager.moveItem(atPath: filePath, toPath: newFilePath)
                    print("Renamed: \(file) -> \(newFilename)")
                    
                    // Log the old and new file paths
                    if let logFile = logFile {
                        let logEntry = "\(filePath) -> \(newFilePath)\n"
                        if let logData = logEntry.data(using: .utf8) {
                            logFile.write(logData)
                        }
                    }
                } else {
                    print("No change needed for: \(file)")
                }
            }
        }
    } catch {
        print("Error: \(error.localizedDescription)")
    }
    
    // Close the log file
    logFile?.closeFile()
}

// Function to prompt user for directory path
func promptForDirectory() -> String {
    print("Please enter the path to the directory you want to clean up:")
    if let input = readLine() {
        return input
    } else {
        print("No input received. Exiting.")
        exit(1)
    }
}

// Main function
func main() {
    let arguments = CommandLine.arguments
    
    // Prompt for directory if no path is provided
    let directory = arguments.count > 1 ? arguments[1] : promptForDirectory()
    print("Renaming files in directory: \(directory)")
    renameFiles(in: directory)
}

main()
