-- Supabase Storage Setup for Voice Web Chat Application
-- Run this in your Supabase SQL Editor after creating the audio-recordings bucket

-- Enable RLS on storage.objects (if not already enabled)
ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist (to avoid conflicts)
DROP POLICY IF EXISTS "Allow authenticated users to upload audio" ON storage.objects;
DROP POLICY IF EXISTS "Allow public access to audio files" ON storage.objects;
DROP POLICY IF EXISTS "Allow users to update their own audio" ON storage.objects;
DROP POLICY IF EXISTS "Allow users to delete their own audio" ON storage.objects;

-- Allow authenticated users to upload audio files
CREATE POLICY "Allow authenticated users to upload audio" ON storage.objects
    FOR INSERT WITH CHECK (
        bucket_id = 'audio-recordings' 
        AND auth.role() = 'authenticated'
    );

-- Allow public access to read audio files (for playback)
CREATE POLICY "Allow public access to audio files" ON storage.objects
    FOR SELECT USING (bucket_id = 'audio-recordings');

-- Allow users to update their own audio files
CREATE POLICY "Allow users to update their own audio" ON storage.objects
    FOR UPDATE USING (
        bucket_id = 'audio-recordings' 
        AND auth.role() = 'authenticated'
    );

-- Allow users to delete their own audio files
CREATE POLICY "Allow users to delete their own audio" ON storage.objects
    FOR DELETE USING (
        bucket_id = 'audio-recordings' 
        AND auth.role() = 'authenticated'
    );

-- Test query to verify bucket exists
SELECT 
    name,
    id,
    public,
    created_at,
    updated_at
FROM storage.buckets 
WHERE name = 'audio-recordings';

-- Test query to check policies
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual,
    with_check
FROM pg_policies 
WHERE tablename = 'objects' 
AND schemaname = 'storage';
