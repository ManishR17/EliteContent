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
    // File upload
    selectedFile: File | null = null;

    // Form fields
    jobDescription: string = '';
    targetRole: string = '';
    experienceLevel: string = 'Mid-Level';
    skillsInput: string = '';
    skillsToHighlight: string[] = [];
    tonePreference: string = 'Professional';
    formatType: string = 'ATS-Friendly';
    additionalAchievements: string = '';

    // State
    isLoading: boolean = false;
    result: any = null;
    error: string = '';

    // Options
    experienceLevels = ['Entry Level', 'Mid-Level', 'Senior', 'Lead', 'Executive'];
    toneOptions = ['Professional', 'Confident', 'Humble', 'Assertive', 'Balanced'];
    formatOptions = ['Minimal', 'ATS-Friendly', 'Modern', 'Executive'];

    constructor(private apiService: ApiService) { }

    onFileSelected(event: any) {
        const file = event.target.files[0];
        if (file) {
            // Validate file type
            const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
            if (validTypes.includes(file.type) || file.name.endsWith('.pdf') || file.name.endsWith('.docx')) {
                this.selectedFile = file;
                this.error = '';
            } else {
                this.error = 'Please upload a PDF or DOCX file.';
                this.selectedFile = null;
            }
        }
    }

    addSkill() {
        if (this.skillsInput.trim()) {
            const skills = this.skillsInput.split(',').map(s => s.trim()).filter(s => s);
            this.skillsToHighlight = [...new Set([...this.skillsToHighlight, ...skills])];
            this.skillsInput = '';
        }
    }

    removeSkill(skill: string) {
        this.skillsToHighlight = this.skillsToHighlight.filter(s => s !== skill);
    }

    generateResume() {
        // Validation
        if (!this.selectedFile) {
            this.error = 'Please upload your resume (PDF or DOCX).';
            return;
        }
        if (!this.jobDescription.trim()) {
            this.error = 'Please enter the job description.';
            return;
        }
        if (!this.targetRole.trim()) {
            this.error = 'Please enter the target role/job title.';
            return;
        }

        this.isLoading = true;
        this.error = '';
        this.result = null;

        this.apiService.generateResume(
            this.selectedFile,
            this.jobDescription,
            this.targetRole,
            this.experienceLevel,
            this.skillsToHighlight,
            this.tonePreference,
            this.formatType,
            this.additionalAchievements || undefined
        ).subscribe({
            next: (response) => {
                this.result = response;
                this.isLoading = false;
            },
            error: (err) => {
                this.error = err.error?.detail || 'Failed to generate resume. Please try again.';
                this.isLoading = false;
                console.error(err);
            }
        });
    }

    downloadResume() {
        if (!this.result?.tailored_resume) return;

        const blob = new Blob([this.result.tailored_resume], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `tailored_resume_${this.targetRole.replace(/\s+/g, '_')}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }
}
