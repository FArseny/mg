const app = new Vue({
    el: "#app",

    data: {
        x: 0,
        y: 0,
        operator: '+',
        first_panel_result: "",
        first_panel_success: true,

        task_id: 0,
        second_panel_result: "",
        second_panel_success: true,

        all_task: [],
    },

    methods: {

        createTaskClickHandler() {
            sendXHR({
                    x: this.x, 
                    y: this.y,
                    operator: this.operator
                },
                "/new_task",
                (resp) => {
                    this.first_panel_success = true;
                    this.first_panel_result = `Created task id = ${resp.task_id}`;
                },
                (resp) => {
                    this.first_panel_success = false;
                    this.first_panel_result = `Errors: ${resp.messages.join('; ')}`;
                }
            );
        },

        checkTaskClickHandler() {

            sendXHR({
                    task_id: this.task_id
                },
                "/check_task",
                (resp) => {
                    this.second_panel_success = true;
                    this.second_panel_result = `Task '${resp.description}' with status '${resp.status}'`
                    if (resp.status == "finished")
                        this.second_panel_result += `; result=${resp.result}`;                    
                },
                (resp) => {
                    this.second_panel_success = false;
                    this.second_panel_result = `Errors: ${resp.messages.join('; ')}`;
                }
            );

        },

        allTaskClickHandler() {

            sendXHR(
                {},
                "/get_all_tasks",
                (resp) => this.all_task = resp.tasks,
                (resp) => {})
        }


    }
})