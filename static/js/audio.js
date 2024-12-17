class AudioManager {
    constructor() {
        this.successSound = new Audio('/static/sounds/seikai.mp3');
        this.failureSound = new Audio('/static/sounds/batu.mp3');
        
        // プリロードして遅延を防ぐ
        this.successSound.load();
        this.failureSound.load();
    }

    async playSuccess() {
        try {
            this.successSound.currentTime = 0;
            await this.successSound.play();
        } catch (error) {
            console.error('Error playing success sound:', error);
        }
    }

    async playFailure() {
        try {
            this.failureSound.currentTime = 0;
            await this.failureSound.play();
        } catch (error) {
            console.error('Error playing failure sound:', error);
        }
    }
}
