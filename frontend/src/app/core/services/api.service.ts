import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({
    providedIn: 'root'
})
export class ApiService {
    private apiUrl = environment.apiUrl;

    constructor(private http: HttpClient) { }

    generateResume(
        file: File,
        jobDescription: string,
        targetRole: string,
        experienceLevel: string,
        skillsToHighlight: string[],
        tonePreference: string,
        formatType: string,
        additionalAchievements?: string
    ): Observable<any> {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('job_description', jobDescription);
        formData.append('target_role', targetRole);
        formData.append('experience_level', experienceLevel);
        formData.append('skills_to_highlight', JSON.stringify(skillsToHighlight));
        formData.append('tone_preference', tonePreference);
        formData.append('format_type', formatType);
        if (additionalAchievements) {
            formData.append('additional_achievements', additionalAchievements);
        }
        return this.http.post(`${this.apiUrl}/resume/generate`, formData);
    }


    generateDocument(data: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/document/generate`, data);
    }

    generateResearch(data: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/research/generate`, data);
    }

    generateCreative(data: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/creative/generate`, data);
    }

    generateEmail(data: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/email/generate`, data);
    }

    generateSocialMedia(data: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/social/generate`, data);
    }

    getDashboardStats(): Observable<any> {
        return this.http.get(`${this.apiUrl}/dashboard/stats`);
    }
}
