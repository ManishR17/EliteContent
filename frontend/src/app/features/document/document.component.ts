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
    // Required Fields
    documentType: string = 'proposal';
    documentTitle: string = '';
    purpose: string = '';
    targetAudience: string = '';
    keyPointsInput: string = '';
    keyPoints: string[] = [];

    // Optional Fields
    toneStyle: string = 'Formal';
    length: string = 'Medium';
    formattingPreference: string = 'Corporate';
    attachmentsDescription: string = '';
    context: string = '';

    isLoading: boolean = false;
    result: any = null;
    error: string = '';

    documentTypes = [
        { value: 'proposal', label: 'Business Proposal' },
        { value: 'report', label: 'Report' },
        { value: 'memo', label: 'Memo' },
        { value: 'cover_letter', label: 'Cover Letter' },
        { value: 'business_plan', label: 'Business Plan' }
    ];

    toneStyles = ['Formal', 'Friendly', 'Technical', 'Persuasive'];
    lengths = ['Short', 'Medium', 'Long'];
    formattingPreferences = ['Simple', 'Corporate', 'Detailed'];

    constructor(private apiService: ApiService) { }

    addKeyPoint() {
        if (this.keyPointsInput.trim()) {
            this.keyPoints.push(this.keyPointsInput.trim());
            this.keyPointsInput = '';
        }
    }

    removeKeyPoint(index: number) {
        this.keyPoints.splice(index, 1);
    }

    generateDocument() {
        if (!this.documentTitle || !this.purpose || !this.keyPointsInput.trim()) {
            this.error = 'Please fill in all required fields.';
            return;
        }

        this.isLoading = true;
        this.error = '';
        this.result = null;

        // Parse key points from textarea (comma or newline separated)
        const keyPoints = this.keyPointsInput
            .split(/[,\n]/)
            .map(point => point.trim())
            .filter(point => point.length > 0);

        const data = {
            document_type: this.documentType,
            document_title: this.documentTitle,
            purpose: this.purpose,
            target_audience: this.targetAudience,
            key_points: keyPoints,
            tone_style: this.toneStyle,
            length: this.length,
            formatting_preference: this.formattingPreference,
            attachments_description: this.attachmentsDescription || undefined,
            context: this.context || undefined
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

        let content = `Title: ${this.documentTitle}\n\n`;
        this.result.sections.forEach((section: any) => {
            content += `${section.title}\n${section.content}\n\n`;
        });

        const blob = new Blob([content], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${this.documentTitle.replace(/\s+/g, '_')}_document.txt`;
        a.click();
        window.URL.revokeObjectURL(url);
    }
}
