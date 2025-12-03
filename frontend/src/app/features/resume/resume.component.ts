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
    // Form fields - REQUIRED
    jobDescription: string = '';
    targetJobTitle: string = '';
    yearsOfExperience: number = 0;
    skillsInput: string = '';
    coreSkills: string[] = [];

    // Form fields - OPTIONAL
    industry: string = '';
    toneStyle: string = 'ATS';
    careerLevel: string = 'Mid';
    achievementsInput: string = '';
    achievements: string[] = [];
    workAuthorization: string = '';
    additionalContext: string = '';
    formatType: string = 'ATS-Friendly';

    // State
    isLoading: boolean = false;
    result: any = null;
    error: string = '';

    // Options
    industries = ['IT', 'Finance', 'Healthcare', 'Marketing', 'Education', 'Manufacturing', 'Retail', 'Other'];
    toneStyles = ['Formal', 'Strong', 'ATS', 'Clean'];
    careerLevels = ['Entry', 'Mid', 'Senior', 'Lead', 'Executive'];
    formatOptions = ['Minimal', 'ATS-Friendly', 'Modern', 'Executive'];

    constructor(private apiService: ApiService) { }

    addSkill() {
        if (this.skillsInput.trim()) {
            const skills = this.skillsInput.split(',').map(s => s.trim()).filter(s => s);
            this.coreSkills = [...new Set([...this.coreSkills, ...skills])];
            this.skillsInput = '';
        }
    }

    removeSkill(skill: string) {
        this.coreSkills = this.coreSkills.filter(s => s !== skill);
    }

    addAchievement() {
        if (this.achievementsInput.trim()) {
            this.achievements.push(this.achievementsInput.trim());
            this.achievementsInput = '';
        }
    }

    removeAchievement(index: number) {
        this.achievements.splice(index, 1);
    }

    generateResume() {
        // Validation
        if (!this.jobDescription || !this.targetJobTitle || !this.skillsInput.trim()) {
            this.error = 'Please fill in all required fields.';
            return;
        }

        this.isLoading = true;
        this.error = '';
        this.result = null;

        // Parse core skills from textarea (comma or newline separated)
        const coreSkills = this.skillsInput
            .split(/[,\n]/)
            .map(skill => skill.trim())
            .filter(skill => skill.length > 0);

        // Parse achievements from textarea (comma or newline separated)
        const achievements = this.achievementsInput
            .split(/[,\n]/)
            .map(ach => ach.trim())
            .filter(ach => ach.length > 0);

        const requestData = {
            job_description: this.jobDescription,
            target_job_title: this.targetJobTitle,
            years_of_experience: this.yearsOfExperience,
            core_skills: coreSkills,
            industry: this.industry || undefined,
            tone_style: this.toneStyle,
            career_level: this.careerLevel,
            achievements: achievements.length > 0 ? achievements : undefined,
            work_authorization: this.workAuthorization || undefined,
            additional_context: this.additionalContext || undefined,
            format_type: this.formatType
        };

        this.apiService.generateResume(requestData).subscribe({
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
        a.download = `tailored_resume_${this.targetJobTitle.replace(/\s+/g, '_')}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }
}
