function generateJSCode(username, password) {
    $.ajax({
        url: "/static/js/cjs.txt",
        method: 'GET',
        xhrFields: {
            responseType: 'text'
        },
        success: function (data) {
            data = data.replaceAll('USR#111CDE$222333#444555$999AAA', username)
            data = data.replaceAll('PWD#111CDE$222333#444555$999AAA', password)
            var obfuscationResult = JavaScriptObfuscator.obfuscate(data, {
                compact: true,
                controlFlowFlattening: true,
                controlFlowFlatteningThreshold: 1,
                numbersToExpressions: true,
                simplify: false,
                shuffleStringArray: true,
                splitStrings: true,
                stringArrayThreshold: 1
            })
            var file = new Blob([obfuscationResult], {type: 'text'});
            var a = document.createElement('a');
            var url = window.URL.createObjectURL(file);
            a.href = url;
            a.download = 'cjs.txt';
            document.body.append(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        },
        failure: function() {
            alert('fail')
        }
    });
}