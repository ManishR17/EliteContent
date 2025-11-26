import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/services/api.service';

@Component({
    selector: 'app-resume',
    standalone: true,
    imports: [CommonModule, FormsModule],
    templateUrl: './resume.component.html',
    styleUrls: ['./resume.component.css']
})
export class ResumeComponent {
    selectedFile: File | null = null;
    jobDescription: string = '';
    isLoading: boolean = false;
    result: any = null;
    error: string = '';

    constructor(private apiService: ApiService) { }

    onFileSelected(event: any) {
        this.selectedFile = event.target.files[0];
    }

    analyzeResume() {
        if (!this.selectedFile || !this.jobDescription) {
            this.error = 'Please upload a resume and enter a job description.';
            return;
        }

        this.isLoading = true;
        this.error = '';
        this.result = null;

        this.apiService.analyzeResume(this.selectedFile, this.jobDescription).subscribe({
            next: (response) => {
                this.result = response;
                this.isLoading = false;
            },
            error: (err) => {
                this.error = 'Failed to analyze resume. Please try again.';
                this.isLoading = false;
                console.error(err);
            }
        });
    }
}
