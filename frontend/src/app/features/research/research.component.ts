import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/services/api.service';

@Component({
    selector: 'app-research',
    standalone: true,
    imports: [CommonModule, FormsModule],
    templateUrl: './research.component.html',
    styleUrls: ['./research.component.css']
})
export class ResearchComponent {
    topic: string = '';
    researchQuestion: string = '';
    citationStyle: string = 'APA';
    length: number = 3000;
    sourcesCount: number = 10;
    isLoading: boolean = false;
    result: any = null;
    error: string = '';

    citationStyles = [
        { value: 'APA', label: 'APA (American Psychological Association)' },
        { value: 'MLA', label: 'MLA (Modern Language Association)' },
        { value: 'Chicago', label: 'Chicago' },
        { value: 'Harvard', label: 'Harvard' },
        { value: 'IEEE', label: 'IEEE (Institute of Electrical and Electronics Engineers)' }
    ];

    lengthOptions = [
        { value: 3000, label: 'Standard (3000 words)' },
        { value: 5000, label: 'Extended (5000 words)' },
        { value: 8000, label: 'Comprehensive (8000 words)' },
        { value: 10000, label: 'Dissertation (10000 words)' }
    ];

    constructor(private apiService: ApiService) { }

    generateResearch() {
        if (!this.topic || !this.researchQuestion) {
            this.error = 'Please enter a topic and research question.';
            return;
        }

        this.isLoading = true;
        this.error = '';
        this.result = null;

        const data = {
            topic: this.topic,
            question: this.researchQuestion,
            citation_style: this.citationStyle,
            length: this.length,
            sources_count: this.sourcesCount
        };

        this.apiService.generateResearch(data).subscribe({
            next: (response) => {
                this.result = response;
                this.isLoading = false;
            },
            error: (err) => {
                this.error = 'Failed to generate research paper. Please try again.';
                this.isLoading = false;
                console.error(err);
            }
        });
    }
}
