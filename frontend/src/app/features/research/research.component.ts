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
    // Required Fields
    topic: string = '';
    researchQuestion: string = '';

    // Optional Fields
    depth: string = 'standard';
    sourcesCount: number = 5;
    citationStyle: string = 'APA';
    academicLevel: string = 'Undergraduate';
    sectionsNeededInput: string = '';
    sectionsNeeded: string[] = [];
    wordCount: number = 1000;
    focusAreasInput: string = '';
    focusAreas: string[] = [];
    sourcesProvidedInput: string = '';
    sourcesProvided: string[] = [];
    includeCitations: boolean = true;

    isLoading: boolean = false;
    result: any = null;
    error: string = '';

    depths = [
        { value: 'quick', label: 'Quick Overview' },
        { value: 'standard', label: 'Standard Research' },
        { value: 'comprehensive', label: 'Comprehensive Deep Dive' }
    ];

    citationStyles = ['APA', 'MLA', 'Chicago', 'Harvard', 'IEEE'];
    academicLevels = ['High School', 'Undergraduate', 'Graduate', 'PhD', 'Professional'];

    constructor(private apiService: ApiService) { }

    addFocusArea() {
        if (this.focusAreasInput.trim()) {
            this.focusAreas.push(this.focusAreasInput.trim());
            this.focusAreasInput = '';
        }
    }

    removeFocusArea(index: number) {
        this.focusAreas.splice(index, 1);
    }

    addSection() {
        if (this.sectionsNeededInput.trim()) {
            this.sectionsNeeded.push(this.sectionsNeededInput.trim());
            this.sectionsNeededInput = '';
        }
    }

    removeSection(index: number) {
        this.sectionsNeeded.splice(index, 1);
    }

    addSource() {
        if (this.sourcesProvidedInput.trim()) {
            this.sourcesProvided.push(this.sourcesProvidedInput.trim());
            this.sourcesProvidedInput = '';
        }
    }

    removeSource(index: number) {
        this.sourcesProvided.splice(index, 1);
    }

    generateResearch() {
        if (!this.topic) {
            this.error = 'Please enter a research topic.';
            return;
        }

        this.isLoading = true;
        this.error = '';
        this.result = null;

        // Parse focus areas from textarea (comma or newline separated)
        const focusAreas = this.focusAreasInput
            .split(/[,\n]/)
            .map(area => area.trim())
            .filter(area => area.length > 0);

        // Parse sections needed from textarea (comma or newline separated)
        const sectionsNeeded = this.sectionsNeededInput
            .split(/[,\n]/)
            .map(section => section.trim())
            .filter(section => section.length > 0);

        // Parse sources provided from textarea (comma or newline separated)
        const sourcesProvided = this.sourcesProvidedInput
            .split(/[,\n]/)
            .map(source => source.trim())
            .filter(source => source.length > 0);

        const data = {
            topic: this.topic,
            research_question: this.researchQuestion || undefined,
            depth: this.depth,
            sources_count: this.sourcesCount,
            citation_style: this.citationStyle,
            academic_level: this.academicLevel,
            sections_needed: sectionsNeeded.length > 0 ? sectionsNeeded : undefined,
            word_count: this.wordCount,
            focus_areas: focusAreas.length > 0 ? focusAreas : undefined,
            sources_provided: sourcesProvided.length > 0 ? sourcesProvided : undefined,
            include_citations: this.includeCitations
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
