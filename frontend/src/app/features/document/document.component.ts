import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/services/api.service';

@Component({
    selector: 'app-document',
    standalone: true,
    imports: [CommonModule, FormsModule],
    templateUrl: './document.component.html',
    styleUrls: ['./document.component.css']
})
export class DocumentComponent {
    documentType: string = 'proposal';
    topic: string = '';
    targetAudience: string = '';
    keyPoints: string = '';
    tone: string = 'professional';
    length: string = 'medium';
    isLoading: boolean = false;
    result: any = null;
    error: string = '';

    documentTypes = [
        { value: 'proposal', label: 'Business Proposal' },
        { value: 'report', label: 'Report' },
        { value: 'memo', label: 'Memo' },
        { value: 'letter', label: 'Business Letter' },
        { value: 'whitepaper', label: 'White Paper' }
    ];

    tones = [
        { value: 'professional', label: 'Professional' },
        { value: 'formal', label: 'Formal' },
        { value: 'casual', label: 'Casual' },
        { value: 'persuasive', label: 'Persuasive' }
    ];

    lengths = [
        { value: 'short', label: 'Short (500-1000 words)' },
        { value: 'medium', label: 'Medium (1000-2000 words)' },
        { value: 'long', label: 'Long (2000-3000 words)' }
    ];

    constructor(private apiService: ApiService) { }

    generateDocument() {
        if (!this.topic || !this.keyPoints) {
            this.error = 'Please enter a topic and key points.';
            return;
        }

        this.isLoading = true;
        this.error = '';
        this.result = null;

        const keyPointsArray = this.keyPoints.split('\n').filter(point => point.trim());

        const data = {
            document_type: this.documentType,
            topic: this.topic,
            target_audience: this.targetAudience || 'General Audience',
            key_points: keyPointsArray,
            tone: this.tone,
            length: this.length
        };

        this.apiService.generateDocument(data).subscribe({
            next: (response) => {
                this.result = response;
                this.isLoading = false;
            },
            error: (err) => {
                this.error = 'Failed to generate document. Please try again.';
                this.isLoading = false;
                console.error(err);
            }
        });
    }

    downloadDocument() {
        if (!this.result) return;

        let content = `Title: ${this.topic}\n\n`;
        this.result.sections.forEach((section: any) => {
            content += `${section.title}\n${section.content}\n\n`;
        });

        const blob = new Blob([content], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${this.topic.replace(/\s+/g, '_')}_document.txt`;
        a.click();
        window.URL.revokeObjectURL(url);
    }
}
