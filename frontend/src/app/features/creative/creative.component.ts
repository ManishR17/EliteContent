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
    contentType: string = 'story';
    genre: string = 'sci-fi';
    plotPoints: string = '';
    tone: string = 'suspenseful';
    pov: string = 'third_limited';
    wordCount: string = 'medium';
    isLoading: boolean = false;
    result: any = null;
    error: string = '';

    contentTypes = [
        { value: 'story', label: 'Short Story' },
        { value: 'script', label: 'Script/Screenplay' },
        { value: 'chapter', label: 'Novel Chapter' },
        { value: 'poem', label: 'Poem' }
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
        { value: 'suspenseful', label: 'Suspenseful' },
        { value: 'humorous', label: 'Humorous' },
        { value: 'dark', label: 'Dark/Gritty' },
        { value: 'lighthearted', label: 'Lighthearted' },
        { value: 'dramatic', label: 'Dramatic' },
        { value: 'mysterious', label: 'Mysterious' }
    ];

    povs = [
        { value: 'first', label: 'First Person (I)' },
        { value: 'second', label: 'Second Person (You)' },
        { value: 'third_limited', label: 'Third Person Limited' },
        { value: 'third_omni', label: 'Third Person Omniscient' }
    ];

    lengths = [
        { value: 'flash', label: 'Flash Fiction (1000 words)' },
        { value: 'short', label: 'Short (3000 words)' },
        { value: 'medium', label: 'Medium (5000 words)' },
        { value: 'long', label: 'Long (8000 words)' }
    ];

    constructor(private apiService: ApiService) { }

    generateCreative() {
        if (!this.plotPoints) {
            this.error = 'Please enter some plot points or ideas.';
            return;
        }

        this.isLoading = true;
        this.error = '';
        this.result = null;

        const plotPointsArray = this.plotPoints.split('\n').filter(point => point.trim());

        const data = {
            type: this.contentType,
            genre: this.genre,
            plot_points: plotPointsArray,
            tone: this.tone,
            pov: this.pov,
            length: this.wordCount
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
