const childProcess = require('child_process')
const path = require("path");
const {PythonShell} =require('python-shell');
const readline = require('readline');


const executePython =  (scriptPath, args = []) => {

    return new Promise(async (resolve, reject) => {


        //const command = [scriptPath].concat([args]);
        let options = {
            mode: 'text',
            pythonOptions: ['-u'], // get print results in real-time
            scriptPath: path.join(__dirname, "pythonScripts"), //If you are having python_test.py script in same folder, then it's optional.
            args: args   //An argument which can be accessed in the script using sys.argv[1]
        };

        PythonShell.run(scriptPath, options, function (err, result) {
            if (err) throw err;
            // result is an array consisting of messages collected
            //during execution of script.

            console.log(scriptPath, result);
            resolve(parseInt(result.toString()));
        });
    })
   /* const python = childProcess.spawn(
            'python',
            command
        );
        let output = "";
        python.stdout.on('data', function(data){
            output += data ;
            console.log("DEBUG PYTHON OUTPUT", data.toString());
        });

        python.stdout.on('close', (code) => {
            return output
        });*/

}

exports.value = async (domain) => {
    let ratio = 10 - (1 - await executePython("searchInGoogle.py", domain)) * 2;
       ratio -= (1 - await executePython("analyzeWhoIs.py", domain)) * 3
       ratio -= (1 - await executePython("analyzeSimilar.py", domain)) * 6
       ratio -= (1 - await executePython("fraudmarkerscheker.py", domain)) * 4


    return ratio>=0?ratio:0
}

