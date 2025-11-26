import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/services/api.service';

@Component({
    selector: 'app-email',
    standalone: true,
    imports: [CommonModule, FormsModule],
    templateUrl: './email.component.html',
    styleUrls: ['./email.component.css']
})
export class EmailComponent {
    emailType: string = 'professional';
    recipient: string = '';
    subject: string = '';
    keyPoints: string = '';
    tone: string = 'professional';
    length: string = 'medium';
    isLoading: boolean = false;
    result: any = null;
    error: string = '';

    emailTypes = [
        { value: 'professional', label: 'Professional Email' },
        { value: 'cold_outreach', label: 'Cold Outreach' },
        { value: 'follow_up', label: 'Follow-up Email' },
        { value: 'thank_you', label: 'Thank You Email' },
        { value: 'introduction', label: 'Introduction Email' },
        { value: 'newsletter', label: 'Newsletter' },
        { value: 'sales', label: 'Sales Email' },
        { value: 'apology', label: 'Apology Email' }
    ];

    tones = [
        { value: 'professional', label: 'Professional' },
        { value: 'friendly', label: 'Friendly' },
        { value: 'formal', label: 'Formal' },
        { value: 'casual', label: 'Casual' },
        { value: 'persuasive', label: 'Persuasive' },
        { value: 'apologetic', label: 'Apologetic' }
    ];

    lengths = [
        { value: 'short', label: 'Short (50-100 words)' },
        { value: 'medium', label: 'Medium (100-200 words)' },
        { value: 'long', label: 'Long (200-300 words)' }
    ];

    constructor(private apiService: ApiService) { }

    generateEmail() {
        if (!this.subject.trim() || !this.keyPoints.trim()) {
            this.error = 'Please enter a subject and key points';
            return;
        }

        this.isLoading = true;
        this.error = '';
        this.result = null;

        const keyPointsArray = this.keyPoints.split('\n').filter(point => point.trim());

        const data = {
            email_type: this.emailType,
            recipient: this.recipient,
            subject: this.subject,
            key_points: keyPointsArray,
            tone: this.tone,
            length: this.length
        };

        this.apiService.generateEmail(data).subscribe({
            next: (response) => {
                this.result = response;
                this.isLoading = false;
            },
            error: (err) => {
                this.error = 'Failed to generate email. Please try again.';
                this.isLoading = false;
                console.error(err);
            }
        });
    }

    copyToClipboard() {
        if (this.result?.email) {
            navigator.clipboard.writeText(this.result.email);
        }
    }

    reset() {
        this.emailType = 'professional';
        this.recipient = '';
        this.subject = '';
        this.keyPoints = '';
        this.tone = 'professional';
        this.length = 'medium';
        this.result = null;
        this.error = '';
    }
}
