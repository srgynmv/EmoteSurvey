function hasGetUserMedia() {
    return !!(navigator.mediaDevices &&
        navigator.mediaDevices.getUserMedia);
}

Vue.options.delimiters = ["[[", "]]"]

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
    props: ['swapComponent', 'mediaRecorder'],
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
            console.log(this.result)
            this.stopRecord()
                .then((result) => {
                    console.log(result.videoUrl)
                    let questions = this.questions
                    let nextQuestionIdx = questions.indexOf(this.currentQuestion) + 1
                    if (nextQuestionIdx < questions.length) {
                        this.setCurrentQuestion(questions[nextQuestionIdx])
                    }
                    else {
                        this.swapComponent('survey-thanks')
                    }
                })
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
                    const videoUrl = URL.createObjectURL(videoBlob)
                    chunks = []
                    resolve({ videoBlob, videoUrl })
                }

                this.mediaRecorder.stop()
            })

        axios.get('/api/questions')
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
        mediaRecorder: null
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
