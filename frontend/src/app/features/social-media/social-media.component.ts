import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/services/api.service';

@Component({
    selector: 'app-social-media',
    standalone: true,
    imports: [CommonModule, FormsModule],
    templateUrl: './social-media.component.html',
    styleUrls: ['./social-media.component.css']
})
export class SocialMediaComponent {
    platform: string = 'linkedin';
    contentType: string = 'post';
    topic: string = '';
    keyPoints: string = '';
    tone: string = 'professional';
    includeHashtags: boolean = true;
    includeEmojis: boolean = true;
    targetLength: string = 'medium';
    isLoading: boolean = false;
    result: any = null;
    error: string = '';

    platforms = [
        { value: 'linkedin', label: 'LinkedIn', icon: '💼', maxLength: 3000 },
        { value: 'twitter', label: 'Twitter/X', icon: '🐦', maxLength: 280 },
        { value: 'instagram', label: 'Instagram', icon: '📸', maxLength: 2200 },
        { value: 'facebook', label: 'Facebook', icon: '👥', maxLength: 63206 },
        { value: 'tiktok', label: 'TikTok', icon: '🎵', maxLength: 2200 }
    ];

    contentTypes = [
        { value: 'post', label: 'Regular Post' },
        { value: 'announcement', label: 'Announcement' },
        { value: 'question', label: 'Question/Poll' },
        { value: 'story', label: 'Story' },
        { value: 'promotional', label: 'Promotional' },
        { value: 'educational', label: 'Educational' },
        { value: 'engagement', label: 'Engagement Post' }
    ];

    tones = [
        { value: 'professional', label: 'Professional' },
        { value: 'casual', label: 'Casual' },
        { value: 'friendly', label: 'Friendly' },
        { value: 'inspirational', label: 'Inspirational' },
        { value: 'humorous', label: 'Humorous' },
        { value: 'authoritative', label: 'Authoritative' }
    ];

    lengthOptions = [
        { value: 'short', label: 'Short' },
        { value: 'medium', label: 'Medium' },
        { value: 'long', label: 'Long' }
    ];

    constructor(private apiService: ApiService) { }

    get selectedPlatform() {
        return this.platforms.find(p => p.value === this.platform);
    }

    generateContent() {
        if (!this.topic.trim()) {
            this.error = 'Please enter a topic';
            return;
        }

        this.isLoading = true;
        this.error = '';
        this.result = null;

        const keyPointsArray = this.keyPoints ? this.keyPoints.split('\n').filter(point => point.trim()) : [];

        const data = {
            platform: this.platform,
            content_type: this.contentType,
            topic: this.topic,
            key_points: keyPointsArray,
            tone: this.tone,
            include_hashtags: this.includeHashtags,
            include_emojis: this.includeEmojis,
            target_length: this.targetLength
        };

        this.apiService.generateSocialMedia(data).subscribe({
            next: (response) => {
                this.result = response;
                this.isLoading = false;
            },
            error: (err) => {
                this.error = 'Failed to generate social media content. Please try again.';
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
        this.platform = 'linkedin';
        this.contentType = 'post';
        this.topic = '';
        this.keyPoints = '';
        this.tone = 'professional';
        this.includeHashtags = true;
        this.includeEmojis = true;
        this.targetLength = 'medium';
        this.result = null;
        this.error = '';
    }
}
