import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/services/api.service';

@Component({
    selector: 'app-creative',
    standalone: true,
    imports: [CommonModule, FormsModule],
    templateUrl: './creative.component.html',
    styleUrls: ['./creative.component.css']
})
export class CreativeComponent {
    // Required Fields
    contentType: string = 'story';
    topic: string = '';
    targetAudience: string = '';

    // Optional Fields
    genre: string = '';
    mainCharactersInput: string = '';
    mainCharacters: string[] = [];
    plotIdea: string = '';
    setting: string = '';
    writingStyle: string = 'Descriptive';
    tone: string = 'Suspenseful';
    length: string = 'Medium';
    dialogueHeavy: boolean = false;
    keywordsInput: string = '';
    keywords: string[] = [];

    isLoading: boolean = false;
    result: any = null;
    error: string = '';

    contentTypes = [
        { value: 'story', label: 'Short Story' },
        { value: 'script', label: 'Script/Screenplay' },
        { value: 'chapter', label: 'Novel Chapter' },
        { value: 'poem', label: 'Poem' },
        { value: 'blog', label: 'Creative Blog' },
        { value: 'lyrics', label: 'Song Lyrics' }
    ];

    genres = [
        { value: 'sci-fi', label: 'Science Fiction' },
        { value: 'fantasy', label: 'Fantasy' },
        { value: 'mystery', label: 'Mystery' },
        { value: 'thriller', label: 'Thriller' },
        { value: 'romance', label: 'Romance' },
        { value: 'horror', label: 'Horror' },
        { value: 'drama', label: 'Drama' },
        { value: 'comedy', label: 'Comedy' }
    ];

    tones = [
        { value: 'Suspenseful', label: 'Suspenseful' },
        { value: 'Humorous', label: 'Humorous' },
        { value: 'Dark', label: 'Dark/Gritty' },
        { value: 'Lighthearted', label: 'Lighthearted' },
        { value: 'Dramatic', label: 'Dramatic' },
        { value: 'Mysterious', label: 'Mysterious' },
        { value: 'Inspirational', label: 'Inspirational' }
    ];

    writingStyles = ['Descriptive', 'Minimalist', 'Flowery', 'Fast-paced', 'Dialogue-driven'];
    lengths = ['Short', 'Medium', 'Long'];

    constructor(private apiService: ApiService) { }

    addCharacter() {
        if (this.mainCharactersInput.trim()) {
            this.mainCharacters.push(this.mainCharactersInput.trim());
            this.mainCharactersInput = '';
        }
    }

    removeCharacter(index: number) {
        this.mainCharacters.splice(index, 1);
    }

    addKeyword() {
        if (this.keywordsInput.trim()) {
            this.keywords.push(this.keywordsInput.trim());
            this.keywordsInput = '';
        }
    }

    removeKeyword(index: number) {
        this.keywords.splice(index, 1);
    }

    generateContent() {
        if (!this.topic || !this.targetAudience) {
            this.error = 'Please enter a topic and target audience.';
            return;
        }

        this.isLoading = true;
        this.error = '';
        this.result = null;

        // Parse main characters from textarea (comma or newline separated)
        const mainCharacters = this.mainCharactersInput
            .split(/[,\n]/)
            .map(char => char.trim())
            .filter(char => char.length > 0);

        // Parse keywords from textarea (comma or newline separated)
        const keywords = this.keywordsInput
            .split(/[,\n]/)
            .map(kw => kw.trim())
            .filter(kw => kw.length > 0);

        const data = {
            content_type: this.contentType,
            topic: this.topic,
            target_audience: this.targetAudience,
            genre: this.genre || undefined,
            main_characters: mainCharacters.length > 0 ? mainCharacters : undefined,
            plot_idea: this.plotIdea || undefined,
            setting: this.setting || undefined,
            writing_style: this.writingStyle,
            tone: this.tone,
            length: this.length,
            dialogue_heavy: this.dialogueHeavy,
            keywords: keywords.length > 0 ? keywords : undefined
        };

        this.apiService.generateCreative(data).subscribe({
            next: (response) => {
                this.result = response;
                this.isLoading = false;
            },
            error: (err) => {
                this.error = 'Failed to generate creative content. Please try again.';
                this.isLoading = false;
                console.error(err);
            }
        });
    }
}
