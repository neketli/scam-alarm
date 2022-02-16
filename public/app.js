import Vue from 'https://cdn.jsdelivr.net/npm/vue@2.6.12/dist/vue.esm.browser.js'

Vue.component('loader', {
    template: `
    <div style="display: flex; justify-content: center; align-items: center;">
        <div class="spinner-border" role="status">
            <span class="">_Загрузка </span>
        </div>
    </div>
    `
})


new Vue({
    el: '#app',
    data() {
        return {
            form: {
                address: '',
                value: ''
            },
            urls: [],
			isLoading: false
        }
    },
    methods:{
        createTr(url, rank){
            const {...obj} = this.form
            obj.value = rank * 10
            this.urls.push(url)
            console.log(obj)
            this.form.address = ''
        },
        getOne(button){
			button.preventDefault();
			this.isLoading = true
            let textInput = document.getElementById("checkDomen").value;
            fetch('/api/rate/one', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({domain: textInput})

            })
                .then((response) => {
                    return response.json();
                })
                .then((response) => {
                    this.urls.push({address: textInput, value: response.ratio })
					this.isLoading = false
                })
				

        },
        getCsv(button){
			button.preventDefault();
			this.isLoading = true
            let fileInput = document.getElementById("fileInput");
            let formData = new FormData()
            formData.append("filedata", fileInput.files[0])
            fetch('/api/rate/file', {
                method: 'POST',
                body: formData
            })
                .then((response) => {
					this.isLoading = false
                        return response.json();
                })
                .then((json) => {
                    this.posts = json
                    Object.keys(json).map((key) => {
                        this.urls.push({address: key, value: json[key]})
                    })

                    this.urls.sort((a, b) => {
                        return a.value > b.value;
                    }).reverse()
                    console.log(json)
					this.isLoading = false
                    this.form.address = ''
                })
                .catch((error) => {
                    console.log(error);
                })
        }
    }
})


