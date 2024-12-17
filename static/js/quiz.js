class QuizGame {
    constructor() {
        this.idioms = [];
        this.currentQuestion = 0;
        this.score = 0;
        this.questionsPerRound = 10;
        this.missedQuestions = [];
        this.audioManager = new AudioManager();
        
        this.loadIdioms().then(() => this.initializeGame());
        this.bindEventListeners();
    }

    async loadIdioms() {
        try {
            const response = await fetch('/api/idioms');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            if (!data.idioms || !Array.isArray(data.idioms)) {
                throw new Error('Invalid idioms data format');
            }
            this.idioms = this.shuffleArray([...data.idioms]);
            return true;
        } catch (error) {
            console.error('Error loading idioms:', error);
            return false;
        }
    }

    bindEventListeners() {
        const restartBtn = document.getElementById('restartBtn');
        if (restartBtn) {
            restartBtn.addEventListener('click', () => this.restartGame());
        }
    }

    async initializeGame() {
        const loaded = await this.loadIdioms();
        if (!loaded || this.idioms.length === 0) {
            document.getElementById('phrase').textContent = 'Error loading idioms data';
            return;
        }
        this.currentQuestion = 0;
        this.score = 0;
        this.missedQuestions = [];
        this.questionsPerRound = Math.min(10, this.idioms.length);
        this.updateProgress();
        this.showQuestion();
    }

    shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }

    getRandomChoices(correctAnswer) {
        let choices = [correctAnswer];
        let otherIdioms = this.idioms.filter(idiom => idiom.meaning !== correctAnswer);
        otherIdioms = this.shuffleArray(otherIdioms);
        choices = choices.concat(otherIdioms.slice(0, 3).map(idiom => idiom.meaning));
        return this.shuffleArray(choices);
    }

    showQuestion() {
        const currentIdiom = this.idioms[this.currentQuestion];
        const choices = this.getRandomChoices(currentIdiom.meaning);
        
        document.getElementById('phrase').textContent = currentIdiom.phrase;
        document.getElementById('example').textContent = currentIdiom.example;
        const choicesContainer = document.getElementById('choices');
        choicesContainer.innerHTML = '';
        
        choices.forEach(choice => {
            const button = document.createElement('button');
            button.className = 'btn choice-btn';
            button.textContent = choice;
            button.addEventListener('click', () => this.checkAnswer(choice, currentIdiom.meaning, button));
            choicesContainer.appendChild(button);
        });
    }

    async checkAnswer(selectedAnswer, correctAnswer, button) {
        const buttons = document.querySelectorAll('.choice-btn');
        buttons.forEach(btn => btn.disabled = true);

        if (selectedAnswer === correctAnswer) {
            button.classList.add('correct', 'animate__animated', 'animate__pulse');
            this.score++;
            await this.audioManager.playSuccess();
        } else {
            button.classList.add('incorrect', 'animate__animated', 'animate__shake');
            const correctButton = Array.from(buttons).find(btn => btn.textContent === correctAnswer);
            correctButton.classList.add('correct');
            this.missedQuestions.push(this.idioms[this.currentQuestion]);
            await this.audioManager.playFailure();
        }

        setTimeout(() => this.nextQuestion(), 1500);
    }

    nextQuestion() {
        this.currentQuestion++;
        this.updateProgress();

        if (this.currentQuestion < this.questionsPerRound) {
            this.showQuestion();
        } else {
            this.showResults();
        }
    }

    updateProgress() {
        const progress = (this.currentQuestion / this.questionsPerRound) * 100;
        document.getElementById('progressBar').style.width = `${progress}%`;
        document.getElementById('score').textContent = `スコア: ${this.score}/${this.currentQuestion}`;
    }

    showResults() {
        document.getElementById('quizContainer').classList.add('d-none');
        document.getElementById('resultContainer').classList.remove('d-none');
        document.getElementById('finalScore').textContent = `${this.score}/${this.questionsPerRound}`;

        const missedQuestionsContainer = document.getElementById('missedQuestions');
        missedQuestionsContainer.innerHTML = '<h4 class="mb-3">間違えた問題:</h4>';
        
        this.missedQuestions.forEach(question => {
            const div = document.createElement('div');
            div.className = 'missed-question';
            div.innerHTML = `
                <strong>${question.phrase}</strong><br>
                意味: ${question.meaning}<br>
                例文: ${question.example}
            `;
            missedQuestionsContainer.appendChild(div);
        });
    }

    restartGame() {
        document.getElementById('quizContainer').classList.remove('d-none');
        document.getElementById('resultContainer').classList.add('d-none');
        this.initializeGame();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new QuizGame();
});
