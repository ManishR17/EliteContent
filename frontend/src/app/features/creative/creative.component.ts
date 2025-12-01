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
    topic: string = '';
    tone: string = 'suspenseful';
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

    creativityLevel: string = 'medium';
    targetAudience: string = '';
    additionalInstructions: string = '';

    constructor(private apiService: ApiService) { }

    generateContent() {
        if (!this.topic) {
            this.error = 'Please enter a topic.';
            return;
        }

        this.isLoading = true;
        this.error = '';
        this.result = null;

        const data = {
            content_type: this.contentType,
            topic: this.topic,
            style: this.creativityLevel, // Mapping creativity level to style
            target_audience: this.targetAudience || 'General Audience',
            length: 'medium', // Default length
            tone: this.tone,
            keywords: this.additionalInstructions ? [this.additionalInstructions] : []
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
