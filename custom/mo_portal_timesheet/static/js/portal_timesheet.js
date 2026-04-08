$(document).ready(function () {
    var projectSelector = $('#project');
    var taskSelector = $('#taskId');

    if (typeof projectSelector.select2 === 'function') {
        projectSelector.select2();
    }
    if (typeof taskSelector.select2 === 'function') {
        taskSelector.select2();
    }

    projectSelector.on('change', function () {
        var projectId = projectSelector.val();
        if (projectId) {
            fetch('/get_project_tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'call',
                    params: { project_id: projectId },
                }),
            })
            .then(function (response) { return response.json(); })
            .then(function (data) {
                var tasks = (data.result && data.result.tasks) || [];
                taskSelector.empty();
                tasks.forEach(function (task) {
                    taskSelector.append(
                        $('<option>', { value: task.id, text: task.name })
                    );
                });
            })
            .catch(function (error) {
                console.error('Error fetching tasks:', error);
            });
        }
    });
});