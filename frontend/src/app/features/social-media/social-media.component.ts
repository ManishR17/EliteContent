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
    // Required Fields
    platform: string = 'linkedin';
    topic: string = '';
    keyMessage: string = '';

    // Optional Fields
    contentType: string = 'post';
    tone: string = 'Professional';
    length: string = 'Medium';
    targetAudience: string = '';
    includeHashtags: boolean = true;
    includeEmoji: boolean = true;
    callToAction: string = '';

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
        { value: 'Professional', label: 'Professional' },
        { value: 'Casual', label: 'Casual' },
        { value: 'Friendly', label: 'Friendly' },
        { value: 'Inspirational', label: 'Inspirational' },
        { value: 'Humorous', label: 'Humorous' },
        { value: 'Authoritative', label: 'Authoritative' }
    ];

    lengths = ['Short', 'Medium', 'Long'];

    constructor(private apiService: ApiService) { }

    get selectedPlatform() {
        return this.platforms.find(p => p.value === this.platform);
    }

    generateContent() {
        if (!this.topic.trim() || !this.keyMessage.trim()) {
            this.error = 'Please enter a topic and key message';
            return;
        }

        this.isLoading = true;
        this.error = '';
        this.result = null;

        const data = {
            platform: this.platform,
            topic: this.topic,
            key_message: this.keyMessage,
            content_type: this.contentType,
            tone: this.tone,
            length: this.length,
            target_audience: this.targetAudience || undefined,
            include_hashtags: this.includeHashtags,
            include_emoji: this.includeEmoji,
            call_to_action: this.callToAction || undefined
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
        this.keyMessage = '';
        this.tone = 'Professional';
        this.length = 'Medium';
        this.targetAudience = '';
        this.includeHashtags = true;
        this.includeEmoji = true;
        this.callToAction = '';
        this.result = null;
        this.error = '';
    }
}
