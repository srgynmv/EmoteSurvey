function hasGetUserMedia() {
    return !!(navigator.mediaDevices &&
        navigator.mediaDevices.getUserMedia);
}

Vue.options.delimiters = ["[[", "]]"]
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

Vue.component('survey-greet', {
    template: `
    <div class="content-box">
        <div class="content" v-html="content"></div>
        <div class="content-footer">
            <button class="accept-button" @click="start">START SURVEY</button>
        </div>
    </div>`,
    props: ['start'],
    data: function () {
        return {
            content: "Welcome to Survey! Please allow access to the camera for analysis of test data."
        }
    },
})

Vue.component('survey-question', {
    template: `
    <div class="content-box">
        <div>
            <div class="content" v-html="content"></div>
            <div class="content" v-if="type === 'single'">
                <div v-for="answer in answers">
                <label>
                    <input type="radio" v-model="result" :value="answer">
                    [[ answer ]]
                </label>
                </div>
            </div>
            <div class="content" v-if="type === 'multiple'">
                <div v-for="answer in answers">
                <label>
                    <input type="checkbox" v-model="result" :value="answer">
                    [[ answer ]]
                </label>
                </div>
            </div>
            <div class="content" v-if="type === 'text'">
                <input type="text" placeholder="Type answer here" v-model="result">
            </div>
            <div class="content-footer">
                <button class="accept-button" v-bind:disabled=isSubmitButtonDisabled @click="submitResult">
                    <span v-if=last>SUBMIT AND FINISH</span>
                    <span v-else>SUBMIT AND NEXT</span>
                </button>
            </div>
        </div>
    </div>`,
    props: ['swapComponent', 'mediaRecorder', 'videoSavingEnabled'],
    data: function () {
        return {
            content: 'Loading...',
            type: null,
            answers: [],
            result: null,
            last: false
        }
    },
    computed: {
        isSubmitButtonDisabled: function () {
            return this.result === null
        }
    },
    methods: {
        setCurrentQuestion(question) {
            this.currentQuestion = question
            this.content = question.text
            this.type = question.type
            this.answers = question.answers
            this.last = question === this.questions[this.questions.length - 1]

            switch (this.type) {
                case 'text':
                    this.result = ''
                    break
                case 'multiple':
                    this.result = []
                    break
                default:
                    this.result = null
            }
            this.startRecord()
        },
        submitResult() {
            this.stopRecord()
                .then(videoBlob => {
                    let questions = this.questions
                    let currentQuestionIdx = questions.indexOf(this.currentQuestion)

                    if (this.videoSavingEnabled) {
                        console.log(this.result)
                        this.downloadFile(videoBlob, `question-${currentQuestionIdx}.webm`)
                    }

                    let questionId = this.currentQuestion.id
                    let answers = typeof(this.result) === 'string' ? [this.result] : this.result
                    let reader = new FileReader()
                    reader.onloadend = function() {
                        axios.post('/api/results/', {
                            question: questionId,
                            answers: answers,
                            recordedData: reader.result,
                        })
                    }
                    reader.readAsDataURL(videoBlob)

                    let nextQuestionIdx = currentQuestionIdx + 1
                    if (nextQuestionIdx < questions.length) {
                        this.setCurrentQuestion(questions[nextQuestionIdx])
                    }
                    else {
                        this.swapComponent('survey-thanks')
                    }
                })
        },
        downloadFile(blob, fileName) {
            let a = document.createElement('a')
            document.body.appendChild(a)
            a.style = 'display: none'
            url = URL.createObjectURL(blob)
            a.href = url
            a.download = fileName
            a.click()
            document.body.removeChild(a)
            URL.revokeObjectURL(url)
        }
    },
    mounted() {
        var chunks = []
        this.mediaRecorder.ondataavailable = (e) => {
            chunks.push(e.data);
        }

        this.startRecord = () => this.mediaRecorder.start()

        this.stopRecord = () =>
            new Promise(resolve => {
                if (this.mediaRecorder.state === 'inactive') {
                    resolve({})
                }

                this.mediaRecorder.onstop = () => {
                    const videoBlob = new Blob(chunks, {type: 'video/webm'})
                    chunks = []
                    resolve(videoBlob)
                }

                this.mediaRecorder.stop()
            })

        axios.get('/api/questions/')
            .then(response => {
                this.questions = response.data
                this.setCurrentQuestion(this.questions[0])
            })
    },
})

Vue.component('survey-thanks', {
    template: `
    <div class="content-box">
        <div class="content" v-html="content"></div>
        <div class="content-footer">
            <button class="accept-button" @click="swapComponent('survey-question')">START AGAIN</button>
        </div>
    </div>`,
    props: ['swapComponent'],
    data: function () {
        return {
            content: "Thanks for answering the survey! If you want to pass it again, click the button below."
        }
    },
})

var app = new Vue({
    el: '#app',
    data: {
        currentComponent: 'survey-greet',
        mediaRecorder: null,
        videoSavingEnabled: false
    },
    methods: {
        swapComponent: function (component) {
            this.currentComponent = component
        },
        start: function () {
            const constraints = {
                video: true
            };

            if (!hasGetUserMedia()) {
                alert('getUserMedia() is not supported by your browser')
                return
            }

            navigator.mediaDevices.getUserMedia(constraints)
                .then((stream) => {
                    var options = {
                        mimeType: 'video/webm'
                    }
                    this.mediaRecorder = new MediaRecorder(stream, options)
                    this.swapComponent('survey-question')
                }, function (error) {
                    alert('Cannot get access to the camera.')
                })
        }
    }
});
