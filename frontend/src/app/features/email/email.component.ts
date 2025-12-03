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
    // Required Fields
    emailPurpose: string = '';
    recipientType: string = '';
    keyPointsInput: string = '';
    keyPoints: string[] = [];

    // Optional Fields
    toneStyle: string = 'Professional';
    urgencyLevel: string = 'Normal';
    callToAction: string = '';
    signatureDetails: string = '';
    subjectLinePreference: string = '';
    context: string = '';

    isLoading: boolean = false;
    result: any = null;
    error: string = '';

    recipientTypes = [
        { value: 'hiring_manager', label: 'Hiring Manager' },
        { value: 'colleague', label: 'Colleague' },
        { value: 'client', label: 'Client' },
        { value: 'executive', label: 'Executive' },
        { value: 'team', label: 'Team' },
        { value: 'investor', label: 'Investor' }
    ];

    toneStyles = ['Professional', 'Friendly', 'Formal', 'Direct', 'Empathetic'];
    urgencyLevels = ['Low', 'Normal', 'High', 'Critical'];

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

    generateEmail() {
        if (!this.emailPurpose || !this.recipientType || !this.keyPointsInput.trim()) {
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
            email_purpose: this.emailPurpose,
            recipient_type: this.recipientType,
            key_points: keyPoints,
            tone_style: this.toneStyle,
            urgency_level: this.urgencyLevel,
            call_to_action: this.callToAction || undefined,
            signature_details: this.signatureDetails || undefined,
            subject_line_preference: this.subjectLinePreference || undefined,
            context: this.context || undefined
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
        this.emailPurpose = '';
        this.recipientType = '';
        this.keyPointsInput = '';
        this.keyPoints = [];
        this.toneStyle = 'Professional';
        this.urgencyLevel = 'Normal';
        this.callToAction = '';
        this.signatureDetails = '';
        this.subjectLinePreference = '';
        this.context = '';
        this.result = null;
        this.error = '';
    }
}
