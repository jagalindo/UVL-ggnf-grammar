//npm install llama-tokenizer-js
import llamaTokenizer from 'llama-tokenizer-js'


import fs from 'fs';
import path from 'path';

// Replace this with the actual directory path
const directoryPath = './promnts_source';

// Function that performs an operation and returns an integer
function performOperation(fileContent) {
    return llamaTokenizer.encode(fileContent).length;
}

// Reading directory
fs.readdir(directoryPath, (err, files) => {
    if (err) {
        return console.error('Unable to read directory: ' + err);
    }

    let results = {};

    files.forEach(file => {
        let filePath = path.join(directoryPath, file);

        // Reading each file
        fs.readFile(filePath, 'utf8', (err, content) => {
            if (err) {
                return console.error('Error reading file: ' + filePath + ' - ' + err);
            }

            // Performing the operation
            let result = performOperation(content);
            results[file] = result;

            // Writing to JSON file after processing all files
            if (Object.keys(results).length === files.length) {
                fs.writeFile('results.json', JSON.stringify(results, null, 2), 'utf8', (err) => {
                    if (err) {
                        return console.error('Error writing JSON file: ' + err);
                    }
                    console.log('Results saved to results.json');
                });
            }
        });
    });
});