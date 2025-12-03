import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/services/api.service';

@Component({
    selector: 'app-new-feature',
    standalone: true,
    imports: [CommonModule, FormsModule],
    templateUrl: './new-feature.component.html',
    styleUrls: ['./new-feature.component.css']
})
export class NewFeatureComponent {
    // Form inputs
    inputField: string = '';
    selectField: string = 'option1';

    // State
    isLoading: boolean = false;
    result: any = null;
    error: string = '';

    // Options for select dropdowns
    options = [
        { value: 'option1', label: 'Option 1' },
        { value: 'option2', label: 'Option 2' },
        { value: 'option3', label: 'Option 3' }
    ];

    constructor(private apiService: ApiService) { }

    generateContent() {
        // Validation
        if (!this.inputField.trim()) {
            this.error = 'Please enter required information';
            return;
        }

        this.isLoading = true;
        this.error = '';
        this.result = null;

        const data = {
            input: this.inputField,
            option: this.selectField
        };

        // Replace with your actual API call
        this.apiService.generateResume(data).subscribe({
            next: (response) => {
                this.result = response;
                this.isLoading = false;
            },
            error: (err) => {
                this.error = 'Failed to generate content. Please try again.';
                this.isLoading = false;
                console.error(err);
            }
        });
    }

    copyToClipboard() {
        if (this.result?.content) {
            navigator.clipboard.writeText(this.result.content);
        }
    }

    reset() {
        this.inputField = '';
        this.selectField = 'option1';
        this.result = null;
        this.error = '';
    }
}
