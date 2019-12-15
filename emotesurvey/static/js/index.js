Vue.options.delimiters = ["[[", "]]"]

Vue.component('survey-greet', {
    template: `
    <div class="content-box">
        <div class="content" v-html="content"></div>
        <div class="content-footer">
            <button class="accept-button" @click="swapComponent('survey-question')">START SURVEY</button>
        </div>
    </div>`,
    props: ['swapComponent'],
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
    props: ['swapComponent'],
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
        },
        submitResult() {
            console.log(this.result)
            let questions = this.questions
            let nextQuestionIdx = questions.indexOf(this.currentQuestion) + 1
            if (nextQuestionIdx < questions.length) {
                this.setCurrentQuestion(questions[nextQuestionIdx])
            }
            else {
                this.swapComponent('survey-thanks')
            }
        }
    },
    mounted() {
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
        currentComponent: 'survey-greet'
    },
    methods: {
        swapComponent: function(component) {
          this.currentComponent = component
        }
    }
});
