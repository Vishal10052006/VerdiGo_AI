"""add chat conversations and messages tables

Revision ID: c9d4f1a7e832
Revises: b7f3e9a2c481
"""
from alembic import op
import sqlalchemy as sa


revision = "c9d4f1a7e832"
down_revision = "b7f3e9a2c481"


def upgrade():
    op.create_table(
        "chat_conversations",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("farmer_profile_id", sa.UUID(), nullable=False),
        sa.Column("title", sa.String(150), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["farmer_profile_id"], ["farmer_profiles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_chat_conv_farmer", "chat_conversations", ["farmer_profile_id"])

    op.create_table(
        "chat_messages",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("conversation_id", sa.UUID(), nullable=False),
        sa.Column("role", sa.Enum("USER", "ASSISTANT", "SYSTEM", name="chatroleenum"), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column(
            "intent",
            sa.Enum(
                "CROP_GUIDANCE", "FERTILIZER_ADVICE", "IRRIGATION_ADVICE",
                "PEST_ADVICE", "WEATHER_QUERY", "GENERAL",
                name="chatintentenum",
            ),
            nullable=True,
        ),
        sa.Column("ai_provider", sa.Enum("GEMINI", "OPENAI", name="aiproviderenum"), nullable=True),
        sa.Column("tokens_used", sa.Integer(), nullable=True),
        sa.Column("response_time_ms", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["conversation_id"], ["chat_conversations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_chat_msg_conversation", "chat_messages", ["conversation_id"])
    op.create_index("idx_chat_msg_created", "chat_messages", ["created_at"])


def downgrade():
    op.drop_index("idx_chat_msg_created", table_name="chat_messages")
    op.drop_index("idx_chat_msg_conversation", table_name="chat_messages")
    op.drop_table("chat_messages")
    op.drop_index("idx_chat_conv_farmer", table_name="chat_conversations")
    op.drop_table("chat_conversations")
    sa.Enum(name="chatroleenum").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="chatintentenum").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="aiproviderenum").drop(op.get_bind(), checkfirst=True)