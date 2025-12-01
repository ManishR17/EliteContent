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
    query: string = '';
    depth: string = 'standard';
    focusArea: string = '';
    includeCitations: boolean = true;
    isLoading: boolean = false;
    result: any = null;
    error: string = '';

    depths = [
        { value: 'quick', label: 'Quick Overview' },
        { value: 'standard', label: 'Standard Research' },
        { value: 'comprehensive', label: 'Comprehensive Deep Dive' }
    ];

    constructor(private apiService: ApiService) { }

    generateResearch() {
        if (!this.query) {
            this.error = 'Please enter a research topic.';
            return;
        }

        this.isLoading = true;
        this.error = '';
        this.result = null;

        const data = {
            topic: this.query,
            depth: this.depth,
            sources_count: 5, // Default
            include_citations: this.includeCitations,
            focus_areas: this.focusArea ? [this.focusArea] : []
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
